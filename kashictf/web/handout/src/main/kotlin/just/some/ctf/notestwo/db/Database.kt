package just.some.ctf.notestwo.db

import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.transactions.transaction
import java.security.MessageDigest
import java.security.SecureRandom
import java.io.File

object Users : IntIdTable() {
    val username = varchar("username", 50).uniqueIndex()
    val passwordHash = varchar("password_hash", 64)
}

object Notes : IntIdTable() {
    val userId = integer("user_id").references(Users.id)
    val content = text("content")
    val createdAt = long("created_at")
}

object DatabaseFactory {
    fun init() {
        val database = Database.connect(
            url = "jdbc:h2:mem:notes;DB_CLOSE_DELAY=-1",
            driver = "org.h2.Driver"
        )

        transaction(database) {
            SchemaUtils.create(Users, Notes)

            val ownerPassword =
                ByteArray(32).also { SecureRandom().nextBytes(it) }.joinToString("") { "%02x".format(it) }
            println("Owner password: $ownerPassword")
            val ownerId = Users.insert {
                it[username] = "owner"
                it[passwordHash] = hashPassword(ownerPassword)
            } get Users.id

            val flag = File("/flag.txt").readText() ?: TODO()
            Notes.insert {
                it[userId] = ownerId.value
                it[content] = "Something something $flag"
                it[createdAt] = System.currentTimeMillis()
            }
        }
    }

    fun hashPassword(password: String): String {
        val md = MessageDigest.getInstance("SHA-256")
        val hash = md.digest(password.toByteArray())
        return hash.joinToString("") { "%02x".format(it) }
    }
}

data class User(val id: Int, val username: String)
data class Note(val id: Int, val content: String, val createdAt: Long)

object UserService {
    fun createUser(username: String, password: String): User? = transaction {
        val existing = Users.select(Users.username eq username).singleOrNull()
        if (existing != null) return@transaction null

        val id = Users.insert {
            it[Users.username] = username
            it[passwordHash] = DatabaseFactory.hashPassword(password)
        } get Users.id

        User(id.value, username)
    }

    fun authenticate(username: String, password: String): User? = transaction {
        val row = Users.select(Users.username eq username).singleOrNull() ?: return@transaction null

        if (row[Users.passwordHash] != DatabaseFactory.hashPassword(password)) {
            return@transaction null
        }

        User(row[Users.id].value, row[Users.username])
    }

    fun getUserByUsername(username: String): User? = transaction {
        val row = Users.select(Users.username eq username).singleOrNull() ?: return@transaction null
        User(row[Users.id].value, row[Users.username])
    }
}

object NoteService {
    fun createNote(userId: Int, content: String): Note = transaction {
        val id = Notes.insert {
            it[Notes.userId] = userId
            it[Notes.content] = content
            it[createdAt] = System.currentTimeMillis()
        } get Notes.id

        Note(id.value, content, System.currentTimeMillis())
    }

    fun getUserNotes(userId: Int): List<Note> = transaction {
        Notes.select(Notes.userId eq userId)
            .map { Note(it[Notes.id].value, it[Notes.content], it[Notes.createdAt]) }
    }

    fun deleteUserNote(userId: Int, noteId: Int): Boolean = transaction {
        try {
            Notes.deleteWhere { (Notes.id eq noteId) and (Notes.userId eq userId) }
            true
        } catch (e: Exception) {
            false
        }
    }
}
