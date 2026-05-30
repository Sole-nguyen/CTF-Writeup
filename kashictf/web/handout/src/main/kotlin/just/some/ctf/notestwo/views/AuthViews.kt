package just.some.ctf.notestwo.views

import kotlinx.html.*

fun HTML.loginPage(error: String? = null) {
    head {
        title { +"SecureNotes - Login" }
        style {
            unsafe {
                +"""
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .form-group { margin: 15px 0; }
                    label { display: block; margin-bottom: 5px; color: #666; }
                    input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                    button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                    button:hover { background: #0056b3; }
                    .error { color: red; text-align: center; margin: 10px 0; }
                    .link { text-align: center; margin-top: 15px; }
                    a { color: #007bff; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                """.trimIndent()
            }
        }
    }
    body {
        div(classes = "container") {
            h1 { +"SecureNotes" }
            if (error != null) {
                div(classes = "error") { +error }
            }
            form(action = "/login", method = FormMethod.post) {
                div(classes = "form-group") {
                    label { +"Username" }
                    input(type = InputType.text, name = "username") {
                        required = true
                    }
                }
                div(classes = "form-group") {
                    label { +"Password" }
                    input(type = InputType.password, name = "password") {
                        required = true
                    }
                }
                button(type = ButtonType.submit) { +"Login" }
            }
            div(classes = "link") {
                +"Don't have an account? "
                a(href = "/register") { +"Register" }
            }
        }
    }
}

fun HTML.registerPage(error: String? = null) {
    head {
        title { +"SecureNotes - Register" }
        style {
            unsafe {
                +"""
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .form-group { margin: 15px 0; }
                    label { display: block; margin-bottom: 5px; color: #666; }
                    input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                    button { width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                    button:hover { background: #218838; }
                    .error { color: red; text-align: center; margin: 10px 0; }
                    .link { text-align: center; margin-top: 15px; }
                    a { color: #007bff; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                """.trimIndent()
            }
        }
    }
    body {
        div(classes = "container") {
            h1 { +"Register for SecureNotes" }
            if (error != null) {
                div(classes = "error") { +error }
            }
            form(action = "/register", method = FormMethod.post) {
                div(classes = "form-group") {
                    label { +"Username" }
                    input(type = InputType.text, name = "username") {
                        required = true
                    }
                }
                div(classes = "form-group") {
                    label { +"Password" }
                    input(type = InputType.password, name = "password") {
                        required = true
                    }
                }
                button(type = ButtonType.submit) { +"Register" }
            }
            div(classes = "link") {
                +"Already have an account? "
                a(href = "/login") { +"Login" }
            }
        }
    }
}
