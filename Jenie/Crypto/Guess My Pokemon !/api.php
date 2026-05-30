<?php
session_start();
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Pokemon list and translation helpers
include "pokemon.php";

// Get game duration in seconds (returns int)
function getGameDuration() {
    if (!isset($_SESSION['game_start_time'])) {
        return 0;
    }
    $currentTime = (int)time();
    return $currentTime - $_SESSION['game_start_time'];
}

// Helper function to format duration (accepts int seconds)
function formatDuration($seconds) {
    $totalSeconds = (int)$seconds;
    $hours = (int)floor($totalSeconds / 3600);
    $minutes = (int)floor(($totalSeconds % 3600) / 60);
    $secs = (int)($totalSeconds % 60);
    
    return sprintf('%02d:%02d:%02d', $hours, $minutes, $secs);
}

// Helper function to encrypt Pokemon name with AES-256-CBC and encode in Base64
function encryptPokemonName($pokemonName) {
    // Init AES parameters
    $key = $_SESSION["aes_key"];
    $iv = random_bytes(16);
    
    // Encrypt using AES-256-CBC
    $encrypted = openssl_encrypt(
        $pokemonName,
        'AES-256-CBC',
        $key,
        OPENSSL_RAW_DATA,
        $iv
    );
    
    // Combine IV and encrypted data, then base64 encode
    $combined = $iv . $encrypted;
    return base64_encode($combined);
}

// Helper function for proof-of-work verification
function verifyPoW(array $pow): bool {
    if (!isset($_SESSION['pow'])) return false;

    $s = $_SESSION['pow'];

    if ($s['used']) return false;
    if (time() > $s['expires']) return false;
    if (!hash_equals($s['challenge'], $pow['challenge'])) return false;

    $expectedHash = hash(
        'sha256',
        $pow['challenge'] . (string)$pow['nonce']
    );

    if (!hash_equals($expectedHash, strtolower($pow['hash']))) {
        return false;
    }

    $prefix = str_repeat('0', $s['difficulty']);

    if (!str_starts_with($expectedHash, $prefix)) {
        return false;
    }

    $_SESSION['pow']['used'] = true;
    return true;
}

function getPokemonFrontSprite(string $pokemon): ?string {
    $formatted_pkmn = urlencode(strtolower($pokemon));
    $url = "https://pokeapi.co/api/v2/pokemon/" . $formatted_pkmn . "/";

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_FAILONERROR => true,
        CURLOPT_HTTPHEADER => [
            'Accept: application/json'
        ]
    ]);

    $response = curl_exec($ch);

    if ($response === false) {
        curl_close($ch);
        return null;
    }

    curl_close($ch);

    $data = json_decode($response, true);
    if (!is_array($data)) {
        return null;
    }

    return $data['sprites']['front_default'] ?? null;
}

// Parse request path
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);

// Handle both /api/* and /api.php/* paths (from .htaccess rewrite)
if (preg_match('#/api(?:\.php)?/(.+)$#', $path, $matches)) {
    $endpoint_path = $matches[1];
} else {
    $endpoint_path = '';
}

$path_parts = explode('/', trim($endpoint_path, '/'));

// Route handling
$method = $_SERVER['REQUEST_METHOD'];
$endpoint = !empty($path_parts) ? end($path_parts) : '';

// Initialize language (default: English)
if (!isset($_SESSION['language'])) {
    $_SESSION['language'] = 'en';
}
$lang = $_SESSION['language'];

// Initialize game if needed
if (!isset($_SESSION['target_pokemon'])) {
    $pokemon_list = getPokemonList($lang);
    $_SESSION['target_pokemon'] = $pokemon_list[array_rand($pokemon_list)];
    $_SESSION['target_pokemon_en'] = translatePokemon($_SESSION['target_pokemon'], $lang, 'en');
    // Generate a random AES key
    $_SESSION['aes_key'] = hash('sha256', uniqid(), true);
    // Set game start time
    $_SESSION['game_start_time'] = (int)time();
    // Generate encrypted hint
    $_SESSION['encrypted_hint'] = encryptPokemonName($_SESSION['target_pokemon']);
    $_SESSION['guesses_remaining'] = 3;
    $_SESSION['guesses'] = [];
    $_SESSION['game_won'] = false;
    $_SESSION['game_over'] = false;
}

// POST /api/language - Change language
if ($method === 'POST' && $endpoint === 'language') {
    $data = json_decode(file_get_contents('php://input'), true);
    
    if (!isset($data['language']) || !in_array($data['language'], ['en', 'fr'])) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => 'Invalid language. Use "en" or "fr".'
        ]);
        exit;
    }
    
    $newLang = $data['language'];
    $oldLang = $_SESSION['language'];
    
    // If game is in progress, translate the target Pokemon
    if (isset($_SESSION['target_pokemon'])) {
        $_SESSION['target_pokemon'] = translatePokemon($_SESSION['target_pokemon'], $oldLang, $newLang);
        $_SESSION['target_pokemon_en'] = translatePokemon($_SESSION['target_pokemon'], $newLang, 'en');
        // Regenerate encrypted hint with new language
        $_SESSION['encrypted_hint'] = encryptPokemonName($_SESSION['target_pokemon']);
        
        // Translate all guesses
        $translated_guesses = [];
        foreach ($_SESSION['guesses'] as $guess) {
            $translated_guesses[] = translatePokemon($guess, $oldLang, $newLang);
        }
        $_SESSION['guesses'] = $translated_guesses;
    }
    
    $_SESSION['language'] = $newLang;
    
    $response = [
        'success' => true,
        'language' => $newLang,
        'message' => $newLang === 'fr' ? 'Langue changée en français' : 'Language changed to English'
    ];
    echo json_encode($response);
    exit;
}

// GET /api/language - Get current language
if ($method === 'GET' && $endpoint === 'language') {
    $response = [
        'success' => true,
        'language' => $_SESSION['language']
    ];
    echo json_encode($response);
    exit;
}

// GET /api/uptime - Get game duration (kept for compatibility, but returns game duration)
if ($method === 'GET' && $endpoint === 'uptime') {
    $duration = getGameDuration(); // Returns int
    $startTime = isset($_SESSION['game_start_time']) ? $_SESSION['game_start_time'] : 0; // Returns int (Unix timestamp)
    
    $response = [
        'success' => true,
        'game_duration_seconds' => $duration,
        'game_start_timestamp' => $startTime
    ];
    echo json_encode($response);
    exit;
}

// GET /api/pow-challenge - Proof-of-work challenge generation
if ($method === 'GET' && $endpoint === 'pow-challenge') {

    $challenge = bin2hex(random_bytes(8));
    $difficulty = 5;
    $expires = time() + 60;

    $_SESSION['pow'] = [
        'challenge' => $challenge,
        'difficulty' => $difficulty,
        'expires' => $expires,
        'used' => false
    ];

    echo json_encode([
        'challenge' => $challenge,
        'difficulty' => $difficulty,
        'expires' => $expires
    ]);
    exit;
}


// GET /api/game - Get current game state
if ($method === 'GET' && $endpoint === 'game') {
    $duration = getGameDuration(); // Returns int
    $startTime = isset($_SESSION['game_start_time']) ? $_SESSION['game_start_time'] : 0; // Returns int (Unix timestamp)
    $response = [
        'success' => true,
        'language' => $_SESSION['language'],
        'game_duration_seconds' => $duration,
        'game_start_timestamp' => $startTime,
        'game' => [
            'guesses_remaining' => $_SESSION['guesses_remaining'],
            'guesses' => $_SESSION['guesses'],
            'game_won' => $_SESSION['game_won'],
            'game_over' => $_SESSION['game_over'],
            'target_pokemon' => $_SESSION['game_over'] || $_SESSION['game_won'] ? $_SESSION['target_pokemon'] : null,
            'encrypted_hint' => $_SESSION['encrypted_hint'] ?? null
        ]
    ];
    echo json_encode($response);
    exit;
}

// POST /api/new - Start a new game
if ($method === 'POST' && $endpoint === 'new') {
    $data = json_decode(file_get_contents('php://input'), true);

    // PoW verification
    if (!isset($data['pow']) || !verifyPoW($data['pow'])) {
        http_response_code(429);
        echo json_encode([
            'success' => false,
            'message' => 'Invalid proof of work'
        ]);
        exit;
    }

    $pokemon_list = getPokemonList($lang);
    $_SESSION['target_pokemon'] = $pokemon_list[array_rand($pokemon_list)];
    $_SESSION['target_pokemon_en'] = translatePokemon($_SESSION['target_pokemon'], $lang, 'en');
    // Generate a random AES key
    $_SESSION['aes_key'] = hash('sha256', uniqid(), true);
    // Set game start time
    $_SESSION['game_start_time'] = (int)time();
    // Generate encrypted hint
    $_SESSION['encrypted_hint'] = encryptPokemonName($_SESSION['target_pokemon']);
    $_SESSION['guesses_remaining'] = 3;
    $_SESSION['guesses'] = [];
    $_SESSION['game_won'] = false;
    $_SESSION['game_over'] = false;
    
    $response = [
        'success' => true,
        'message' => $lang === 'fr' ? 'Nouvelle partie démarrée' : 'New game started',
        'language' => $lang,
        'game_duration_seconds' => 0,
        'game_start_timestamp' => $_SESSION['game_start_time'],
        'game' => [
            'guesses_remaining' => $_SESSION['guesses_remaining'],
            'guesses' => $_SESSION['guesses'],
            'game_won' => $_SESSION['game_won'],
            'game_over' => $_SESSION['game_over'],
            'encrypted_hint' => $_SESSION['encrypted_hint']
        ]
    ];
    echo json_encode($response);
    exit;
}

include "flag-58b18554-6221-4ea3-9db8-b520dffd94c4.php";

// POST /api/guess - Submit a guess
if ($method === 'POST' && $endpoint === 'guess') {
    $data = json_decode(file_get_contents('php://input'), true);

    // PoW verification
    if (!isset($data['pow']) || !verifyPoW($data['pow'])) {
        http_response_code(429);
        echo json_encode([
            'success' => false,
            'message' => 'Invalid proof of work'
        ]);
        exit;
    }
    
    // Translations
    $translations = [
        'en' => [
            'empty_guess' => 'Please enter a Pokemon name!',
            'game_over' => 'Game is already over. Start a new game!',
            'invalid_pokemon' => '"%s" is not a valid Pokemon!',
            'already_guessed' => 'You already guessed "%s"!',
            'congratulations' => '🎉 Congratulations! You guessed it! The Pokemon was %s!',
            'game_over_msg' => 'Game Over! The Pokemon was %s. Better luck next time!',
            'wrong_guess' => '❌ Wrong guess! %d guess(es) remaining!'
        ],
        'fr' => [
            'empty_guess' => 'Veuillez entrer un nom de Pokémon !',
            'game_over' => 'La partie est déjà terminée. Commencez une nouvelle partie !',
            'invalid_pokemon' => '"%s" n\'est pas un Pokémon valide !',
            'already_guessed' => 'Vous avez déjà deviné "%s" !',
            'congratulations' => '🎉 Félicitations ! Vous avez trouvé ! Le Pokémon était %s !',
            'game_over_msg' => 'Partie terminée ! Le Pokémon était %s. Bonne chance la prochaine fois !',
            'wrong_guess' => '❌ Mauvaise réponse ! %d tentative(s) restante(s) !'
        ]
    ];
    
    $t = $translations[$lang];
    
    if (!isset($data['guess']) || empty(trim($data['guess']))) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => $t['empty_guess']
        ]);
        exit;
    }
    
    $guess = trim($data['guess']);
    
    // Check if game is over
    if ($_SESSION['game_over'] || $_SESSION['game_won']) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => $t['game_over']
        ]);
        exit;
    }
    
    // Normalize Pokemon name (accept both languages)
    $normalized = normalizePokemonName($guess);
    if ($normalized === null) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => sprintf($t['invalid_pokemon'], htmlspecialchars($guess))
        ]);
        exit;
    }
    
    // Get the name in current language
    $guess_in_lang = $normalized[$lang];
    $guess_normalized = ucfirst(strtolower($guess_in_lang));
    
    // Check if already guessed (check in current language)
    $already_guessed = false;
    foreach ($_SESSION['guesses'] as $prev_guess) {
        if (strcasecmp($prev_guess, $guess_normalized) === 0) {
            $already_guessed = true;
            break;
        }
    }
    
    if ($already_guessed) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => sprintf($t['already_guessed'], htmlspecialchars($guess_normalized))
        ]);
        exit;
    }
    
    // Add to guesses
    $_SESSION['guesses'][] = $guess_normalized;
    
    // Encrypt the guessed Pokemon name
    $encrypted_guess = encryptPokemonName($guess_normalized);
    
    // Check if correct (compare using English names for consistency)
    $target_en = $_SESSION['target_pokemon_en'];
    $guess_en = $normalized['en'];
    $is_correct = (strcasecmp($guess_en, $target_en) === 0);
    
    if ($is_correct) {
        $_SESSION['game_won'] = true;
        $_SESSION['game_over'] = true;
        
        $response = [
            'success' => true,
            'correct' => true,
            'message' => sprintf($t['congratulations'], htmlspecialchars($_SESSION['target_pokemon'])),
            'flag' => $FLAG,
            'encrypted_guess' => $encrypted_guess,
            'game' => [
                'guesses_remaining' => $_SESSION['guesses_remaining'],
                'guesses' => $_SESSION['guesses'],
                'game_won' => true,
                'game_over' => true,
                'target_pokemon' => $_SESSION['target_pokemon'],
                'pokemon_sprite' => getPokemonFrontSprite($_SESSION['target_pokemon_en']),
                'encrypted_hint' => $_SESSION['encrypted_hint']
            ]
        ];
    } else {
        $_SESSION['guesses_remaining']--;
        
        if ($_SESSION['guesses_remaining'] <= 0) {
            $_SESSION['game_over'] = true;
            
            $response = [
                'success' => true,
                'correct' => false,
                'message' => sprintf($t['game_over_msg'], htmlspecialchars($_SESSION['target_pokemon'])),
                'encrypted_guess' => $encrypted_guess,
                'game' => [
                    'guesses_remaining' => 0,
                    'guesses' => $_SESSION['guesses'],
                    'game_won' => false,
                    'game_over' => true,
                    'target_pokemon' => $_SESSION['target_pokemon'],
                    'pokemon_sprite' => getPokemonFrontSprite($_SESSION['target_pokemon_en']),
                    'encrypted_hint' => $_SESSION['encrypted_hint']
                ]
            ];
        } else {
            // Wrong guess
            $response = [
                'success' => true,
                'correct' => false,
                'message' => sprintf($t['wrong_guess'], $_SESSION['guesses_remaining']),
                'encrypted_guess' => $encrypted_guess,
                'game' => [
                    'guesses_remaining' => $_SESSION['guesses_remaining'],
                    'guesses' => $_SESSION['guesses'],
                    'game_won' => false,
                    'game_over' => false,
                    'encrypted_hint' => $_SESSION['encrypted_hint']
                ]
            ];
        }
    }
    
    echo json_encode($response);
    exit;
}

// 404 - Endpoint not found
http_response_code(404);
echo json_encode([
    'success' => false,
    'error' => 'Endpoint not found'
]);
?>
