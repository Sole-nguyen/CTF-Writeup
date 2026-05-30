package just.some.ctf.notestwo

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.html.*
import io.ktor.server.netty.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*
import kotlinx.coroutines.*
import just.some.ctf.notestwo.auth.JwtConfig
import just.some.ctf.notestwo.auth.TokenCache
import just.some.ctf.notestwo.db.*
import just.some.ctf.notestwo.views.*
import kotlinx.serialization.Serializable

@Serializable
data class UserSession(val token: String)

fun Application.module() {
    DatabaseFactory.init()

    install(Sessions) {
        cookie<UserSession>("SESSION") {
            cookie.path = "/"
            cookie.maxAgeInSeconds = 36000
        }
    }

    val cacheScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    val tokenCache = TokenCache(cacheScope)
    tokenCache.start()

    val downloadPermissions = mutableMapOf<String, Long>()

    routing {
        get("/") {
            call.respondRedirect("/login")
        }

        get("/login") {
            val error = call.request.queryParameters["error"]
            call.respondHtml { loginPage(error) }
        }

        post("/login") {
            val params = call.receiveParameters()
            val username = params["username"]
            val password = params["password"]

            if (username.isNullOrBlank() || password.isNullOrBlank()) {
                call.respondRedirect("/login?error=Invalid credentials")
                return@post
            }

            val user = UserService.authenticate(username, password)
            if (user == null) {
                call.respondRedirect("/login?error=Invalid credentials")
                return@post
            }

            if (tokenCache.getCacheSize() >= 10) {
                call.respondText(
                    "503 Response from server: Hang on. I am doing something I told you not to worry about.",
                    status = HttpStatusCode.ServiceUnavailable
                )
                return@post
            }

            val token = JwtConfig.generateToken(user.username)

            tokenCache.cacheToken(token, JwtConfig.verifyToken(token)!!)

            call.sessions.set(UserSession(token))
            call.respondRedirect("/notes")
        }

        get("/register") {
            val error = call.request.queryParameters["error"]
            call.respondHtml { registerPage(error) }
        }

        post("/register") {
            val params = call.receiveParameters()
            val username = params["username"]
            val password = params["password"]

            if (username.isNullOrBlank() || password.isNullOrBlank()) {
                call.respondRedirect("/register?error=Username and password required")
                return@post
            }

            val user = UserService.createUser(username, password)
            if (user == null) {
                call.respondRedirect("/register?error=Username already exists")
                return@post
            }

            if (tokenCache.getCacheSize() >= 10) {
                call.respondText(
                    "503 Response from server: Hang on. I am doing something I told you not to worry about.",
                    status = HttpStatusCode.ServiceUnavailable
                )
                return@post
            }

            val token = JwtConfig.generateToken(user.username)

            tokenCache.cacheToken(token, JwtConfig.verifyToken(token)!!)

            call.sessions.set(UserSession(token))
            call.respondRedirect("/notes")
        }

        post("/logout") {
            val session = call.sessions.get<UserSession>()
            val token = session?.token
            token?.let {
                tokenCache.processLogout(it)
            }
            call.sessions.clear<UserSession>()
            call.respondRedirect("/login")
        }

        get("/notes") {
            val session = call.sessions.get<UserSession>()
            if (session == null) {
                call.respondRedirect("/login")
                return@get
            }

            val claims = tokenCache.verifyToken(session.token)
            if (claims == null) {
                call.sessions.clear<UserSession>()
                call.respondRedirect("/login?error=Session expired")
                return@get
            }

            val username = JwtConfig.getUsername(claims)
            val downloadReady = downloadPermissions[session.token]?.let { grantedTime ->
                grantedTime <= System.currentTimeMillis()
            } ?: false
            val user = UserService.getUserByUsername(username)
            if (user == null) {
                call.sessions.clear<UserSession>()
                call.respondRedirect("/login?error=Session expired")
                return@get
            }
            val notes = NoteService.getUserNotes(user.id)
            call.respondHtml { notesPage(username, notes, downloadReady) }
        }

        post("/notes") {
            val session = call.sessions.get<UserSession>()
            if (session == null) {
                call.respondRedirect("/login")
                return@post
            }

            val claims = tokenCache.verifyToken(session.token)
            if (claims == null) {
                call.sessions.clear<UserSession>()
                call.respondRedirect("/login?error=Session expired")
                return@post
            }

            val username = JwtConfig.getUsername(claims)
            val params = call.receiveParameters()
            val content = params["content"]

            if (!content.isNullOrBlank()) {
                val user = UserService.getUserByUsername(username)
                user?.let {
                    NoteService.createNote(it.id, content)
                }
            }

            call.respondRedirect("/notes")
        }

        post("/notes/{id}/delete") {
            val session = call.sessions.get<UserSession>()
            if (session == null) {
                call.respondRedirect("/login")
                return@post
            }

            val claims = tokenCache.verifyToken(session.token)
            if (claims == null) {
                call.sessions.clear<UserSession>()
                call.respondRedirect("/login?error=Session expired")
                return@post
            }
            val username = JwtConfig.getUsername(claims)
            val noteId = call.parameters["id"]?.toIntOrNull()
            noteId?.let {
                val user = UserService.getUserByUsername(username)
                if (user != null) {
                    NoteService.deleteUserNote(user.id, it)
                }
            }
            call.respondRedirect("/notes")
        }

        post("/notes/request-download") {
            val session = call.sessions.get<UserSession>()
            if (session == null) {
                call.respond(HttpStatusCode.Unauthorized, "Not authenticated")
                return@post
            }

            val claims = tokenCache.verifyToken(session.token)
            if (claims == null) {
                call.respond(HttpStatusCode.Unauthorized, "Invalid session")
                return@post
            }

            val params = call.receiveParameters()
            val requestedUsername = params["username"] ?: ""

            if (downloadPermissions.containsKey(session.token)) {
                val grantedTime = downloadPermissions[session.token]!!
                if (grantedTime <= System.currentTimeMillis()) {
                    val user = UserService.getUserByUsername(requestedUsername)
                    if (user != null) {
                        val notes = NoteService.getUserNotes(user.id)
                        call.respondText(
                            notes.joinToString("\n") { "- ${it.content}" },
                            ContentType.Text.Plain
                        )
                    } else {
                        call.respond(HttpStatusCode.NotFound, "User not found")
                    }
                } else {
                    call.respondText("Your request for data download is being processed, check back in a few moments.")
                }
            } else {
                if (downloadPermissions.size >= 10) {
                    call.respond(HttpStatusCode.ServiceUnavailable, "Download service temporarily unavailable")
                    return@post
                }
                val grantedTime = System.currentTimeMillis() + (300 * 1000)
                downloadPermissions[session.token] = grantedTime
                call.respondText("Your request for data download is being processed, check back in a few moments.")
            }
        }


    }
}

fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
        module()
    }.start(wait = true)
}
