import express from "express";
import { getDB } from "./lib/db.ts";

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("./app"));

type QueryParams = { name?: string; password?: string };

app.get("/actions/login", (req, res) => {
	const db = getDB();

	const query: QueryParams = req.query;
	console.log("query", query);

	// Express query parameters can be non-strings (e.g., arrays when a key is repeated).
	// Always validate types before using them.
	if (!query || typeof query.name !== "string" || typeof query.password !== "string") {
		return res.status(400).send("bad parameters");
	}

	// Parameterized query prevents SQL injection regardless of input content.
	const stmt = db.query("SELECT name FROM users WHERE name = ? AND password = ?");
	const user = stmt.get(query.name, query.password) as { name: string } | null;

	if (!user || !user.name) return res.status(400).send(`Staff not found`);
	return res.send(`Welcome, ${user.name}. You now have access to the restricted archives.`);
});

const port = process.env.PORT ?? "3000";
app.listen(port, () => {
	console.log(`server is listening at localhost:${port}`);
});
