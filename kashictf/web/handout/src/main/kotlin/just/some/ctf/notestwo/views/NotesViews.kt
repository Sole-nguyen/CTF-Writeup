package just.some.ctf.notestwo.views

import kotlinx.html.*
import just.some.ctf.notestwo.db.Note

fun HTML.notesPage(username: String, notes: List<Note>, downloadReady: Boolean) {
    head {
        title { +"SecureNotes - My Notes" }
        style {
            unsafe {
                +"""
                    body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
                    .header { background: #007bff; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
                    .header h1 { margin: 0; font-size: 24px; }
                    .header-right { display: flex; gap: 15px; align-items: center; }
                    .username { font-size: 14px; }
                    .btn { padding: 8px 16px; background: white; color: #007bff; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 14px; }
                    .btn:hover { background: #f0f0f0; }
                    .btn-logout { background: #dc3545; color: white; }
                    .btn-logout:hover { background: #c82333; }
                    .btn-download { background: #28a745; color: white; }
                    .btn-download:hover { background: #218838; }
                    .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
                    .note-form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px; }
                    textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-family: Arial, sans-serif; min-height: 100px; }
                    .btn-primary { width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; }
                    .btn-primary:hover { background: #218838; }
                    .notes-list { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .note-item { padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: start; }
                    .note-item:last-child { border-bottom: none; }
                    .note-content { flex: 1; word-wrap: break-word; }
                    .note-date { color: #999; font-size: 12px; margin-top: 5px; }
                    .btn-delete { padding: 5px 10px; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px; }
                    .btn-delete:hover { background: #c82333; }
                    .empty-state { text-align: center; color: #999; padding: 40px; }
                """.trimIndent()
            }
        }
    }
    body {
        div(classes = "header") {
            h1 { +"SecureNotes" }
            div(classes = "header-right") {
                span(classes = "username") {
                    +"Welcome, $username"
                }
                form(action = "/logout", method = FormMethod.post) {
                    style = "display: inline; margin: 0;"
                    button(type = ButtonType.submit, classes = "btn btn-logout") { +"Logout" }
                }
            }
        }
        div(classes = "container") {
            div(classes = "note-form") {
                h2 { +"Create New Note" }
                form(action = "/notes", method = FormMethod.post) {
                    textArea {
                        name = "content"
                        attributes["placeholder"] = "Write your note here..."
                        attributes["required"] = "required"
                    }
                    button(type = ButtonType.submit, classes = "btn-primary") { +"Add Note" }
                }
            }

            // Download button
            div(classes = "note-form") {
                h3 { +"Export Notes" }
                form(action = "/notes/request-download", method = FormMethod.post) {
                    id = "downloadForm"
                    hiddenInput(name = "username") {
                        value = username
                    }
                    button(type = ButtonType.submit, classes = "btn-primary btn-download") {
                        if (downloadReady) {
                            +"Notes available for download"
                        } else {
                            +"Request notes download"
                        }
                    }
                }
            }

            div(classes = "notes-list") {
                h2 { +"My Notes" }
                if (notes.isEmpty()) {
                    div(classes = "empty-state") { +"No notes yet. Create your first note above!" }
                } else {
                    notes.forEach { note ->
                        div(classes = "note-item") {
                            div {
                                div(classes = "note-content") {
                                    unsafe { +note.content }
                                }
                                div(classes = "note-date") {
                                    +java.text.SimpleDateFormat("MMM dd, yyyy HH:mm")
                                        .format(java.util.Date(note.createdAt))
                                }
                            }
                            form(action = "/notes/${note.id}/delete", method = FormMethod.post) {
                                style = "display: inline;"
                                button(type = ButtonType.submit, classes = "btn-delete") { +"Delete" }
                            }
                        }
                    }
                }
            }
        }
    }
}
