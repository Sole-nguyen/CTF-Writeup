package just.some.ctf.notestwo.auth

import just.some.ctf.notestwo.db.UserService
import io.jsonwebtoken.Claims
import kotlinx.coroutines.*
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.channels.Channel
import java.util.concurrent.ConcurrentHashMap

class TokenCache(private val scope: CoroutineScope) {
    private val cache = ConcurrentHashMap<String, Claims>()
    private val logoutChannel = Channel<String>(capacity = 10, onBufferOverflow = BufferOverflow.DROP_OLDEST)

    fun start() {
        scope.launch {
            while (true) {
                while (!logoutChannel.isEmpty) {
                    val token = logoutChannel.tryReceive().getOrNull()
                    if (token != null) {
                        processLogoutInline(token)
                    }
                }

                delay(5000)

                val now = System.currentTimeMillis()
                val expiredTokens =
                    cache.filter { (_, claims) -> claims.expiration.toInstant().toEpochMilli() < now }.keys

                expiredTokens.forEach { token ->
                    cache.remove(token)
                }
            }
        }
    }

    fun cacheToken(token: String, claims: Claims) {
        cache[token] = claims
    }

    fun processLogout(token: String) {
        val result = logoutChannel.trySend(token)
    }

    private fun processLogoutInline(token: String) {
        // Full validation isn't needed as the user can't impersonate others without token
        JwtConfig.parseWithoutValidation(token)?.let {
            val username = JwtConfig.getUsername(it)
            UserService.getUserByUsername(username).let {
                cache.remove(token)
            }
        }
    }

    fun verifyToken(token: String): Claims? {
        return cache[token]
    }

    fun getCacheSize(): Int = cache.size
}
