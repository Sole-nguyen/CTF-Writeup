// Minimal ambient declarations to satisfy TypeScript in this Bun/Express CTF setup
// without pulling in Node's full type definitions.

declare const process: {
	env: Record<string, string | undefined>;
};
