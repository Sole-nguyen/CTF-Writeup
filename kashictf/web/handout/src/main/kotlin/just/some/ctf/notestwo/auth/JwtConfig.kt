package just.some.ctf.notestwo.auth

import io.jsonwebtoken.Jwts
import io.jsonwebtoken.SignatureAlgorithm
import io.jsonwebtoken.security.Keys
import java.util.Date
import javax.crypto.SecretKey

object JwtConfig {
    private val secret: SecretKey = Keys.secretKeyFor(SignatureAlgorithm.HS256)
    private const val validityInMs = 3 * 60_000

    fun generateToken(username: String): String {
        return Jwts.builder()
            .setSubject(username)
            .setIssuedAt(Date())
            .setExpiration(Date(System.currentTimeMillis() + validityInMs))
            .signWith(secret)
            .compact()
    }

    fun verifyToken(token: String): io.jsonwebtoken.Claims? {
        return try {
            Jwts.parserBuilder()
                .setSigningKey(secret)
                .build()
                .parseClaimsJws(token)
                .body
        } catch (e: Exception) {
            null
        }
    }

    fun parseWithoutValidation(token: String): io.jsonwebtoken.Claims? {
        return try {
            val parts = token.split(".")
            if (parts.size != 3) return null
            val unsignedToken = parts[0] + "." + parts[1] + "."
            Jwts.parserBuilder()
                .build()
                .parseClaimsJwt(unsignedToken)
                .body
        } catch (e: Exception) {
            null
        }
    }

    fun getUsername(claims: io.jsonwebtoken.Claims): String {
        return claims.subject
    }
}
