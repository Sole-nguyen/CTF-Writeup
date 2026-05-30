#!/usr/bin/env python3

import os
import json
import random
import socket
import base64
import logging
import socketserver

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from secret import FLAG


BANNER = b"""\
  ___         _     ___                      ___     _                   
 | _ \\___  __| |__ | _ \\__ _ _ __  ___ _ _  / __| __(_)______ ___ _ _ ___
 |   / _ \\/ _| / / |  _/ _` | '_ \\/ -_) '_| \\__ \\/ _| (_-<_-</ _ \\ '_(_-<
 |_|_\\___/\\__|_\\_\\ |_| \\__,_| .__/\\___|_|   |___/\\__|_/__/__/\\___/_| /__/
                            |_|
                                                   Jeanne d'Hack CTF 2026

          ~~~  Welcome to the Rock-Paper-Scissors game !  ~~~
"""

class RockPaperScissors(socketserver.BaseRequestHandler):

    def __init__(self, *args, **kwargs):
        """
        Server initialization
        """
        self.logger = logging.getLogger("Default")
        self.logger.debug("Rock Paper Scissors instance created")
        # Initialize a secure random generator for server plays
        self.secure_random = random.SystemRandom()
        # Initialize AES cipher
        key = os.urandom(16)
        nonce = os.urandom(16)
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        # Defines games constants
        self.VALID_CHOICES = {
            1: "Play a game",
            2: "View statistics",
            3: "Save progress",
            4: "Load progress",
            5: "Show the flag",
            6: "Exit"
        }
        self.VALID_PLAYS = {
            1: "rock",
            2: "paper",
            3: "scissors"
        }
        self.WINS_AGAINST = {
            1: 3,
            2: 1,
            3: 2
        }
        # Need to be called last otherwise it does not initialize attributes
        super().__init__(*args, **kwargs)

    # Game logic
    
    def handle(self):
        """
        Handle a client connection.
        """
        # Keep track of user games progress
        player_progress = {
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "total_games": 0,
            "winrate": 0.0
        }
        self.request.send(BANNER)
        # Main loop
        try:
            while True:
                self.show_main_menu(self.request)
                try:
                    data = self.request.recv(1024).decode().strip()
                    choice = int(data)
                except ValueError:
                    self.request.send(b"Please enter a number.\n")
                    continue
                
                if choice == 6:
                    self.request.send(b"Bye!\n")
                    break

                self.handle_choice(self.request, choice, player_progress)

        except (ConnectionResetError, BrokenPipeError):
            self.logger.debug("Client disconnected")

        finally:
            self.request.close()


    def show_main_menu(self, client_socket):
        """
        Display the main menu
        """
        client_socket.send(b"\n--- Main Menu ---\n")
        for number, description in self.VALID_CHOICES.items():
            client_socket.send(f"{number}. {description}\n".encode())

        client_socket.send(b"\nChoose your option:\n> ")

    def handle_choice(self, client_socket, choice: int, player_progress: dict):
        """
        Handle client choice
        """
        # Check choice validity
        if choice not in self.VALID_CHOICES.keys():
            client_socket.send(b"\nInvalid choice!\n")
            return
        # Perform chosen action
        if choice == 1:
            self.play_round(client_socket, player_progress)
        elif choice == 2:
            self.view_stats(client_socket, player_progress)
        elif choice == 3:
            self.save_progress(client_socket, player_progress)
        elif choice == 4:
            self.load_progress(client_socket, player_progress)
        else: # choice == 5
            self.show_flag(client_socket, player_progress)

    def play_round(self, client_socket, player_progress):
        """
        Play a rock-paper-scissors round
        """
        # Choose server play
        server_play = self.secure_random.randint(1, 3)
        self.logger.debug("Server play: %s", self.VALID_PLAYS[server_play])
        # Retrieve client play
        client_socket.send(b"\nYour turn:\n")
        for number, play in self.VALID_PLAYS.items():
            client_socket.send(f"{number}. {play}\n".encode())
        
        client_socket.send(b"\n> ")

        try:
            client_play = int(client_socket.recv(1024).decode())
        except ValueError:
            client_socket.send(b"Please enter a number.\n")
            return

        if client_play not in self.VALID_PLAYS.keys():
            client_socket.send(b"\nInvalid play!\n")
            return

        result, msg = self.determine_result(client_play, server_play)
        self.update_stats(result, player_progress)

        client_socket.send(f"\nServer play {self.VALID_PLAYS[server_play]}. {msg}\n".encode())

    def determine_result(self, client_play: int, server_play: int):
        """
        Determine the result of a game and returns a message for the client.
        """
        # Draw case
        if client_play == server_play:
            return 0, "It's a draw."
        # Client wins against server
        if self.WINS_AGAINST[client_play] == server_play:
            return 1, "You win!"
        # Server wins
        return -1, "You lose..."

    def update_stats(self, result: int, player_progress: dict):
        """
        Update player's statistics
        """
        player_progress["total_games"] += 1
        if result > 0:
            player_progress["wins"] += 1
        elif result < 0:
            player_progress["losses"] += 1
        else:
            player_progress["draws"] += 1
        # Update winrate
        winrate = (player_progress["wins"] / player_progress["total_games"]) * 100
        player_progress["winrate"] = round(winrate, 2)

    def view_stats(self, client_socket, player_progress: dict):
        """
        Display player's statistics
        """
        client_socket.send((
            f"\nYour stats:\n"
            + f"  Total games : {player_progress['total_games']}\n"
            + f"  Wins        : {player_progress['wins']}\n"
            + f"  Losses      : {player_progress['losses']}\n"
            + f"  Draws       : {player_progress['draws']}\n"
            + f"  Winrate     : {player_progress['winrate']}%\n"
        ).encode())

    def save_progress(self, client_socket, player_progress: dict):
        """
        Save player's progress
        """
        formatted_save = dict(
            map(lambda kv: (kv[0], f"{kv[1]:03}"), player_progress.items())
        )
        save = json.dumps(formatted_save)
        client_socket.send(f"\nYour actual stats: {save}\n".encode())
        # Encrypt the player's progress to avoid cheating
        encryptor = self.cipher.encryptor()
        secure_save = base64.b64encode(
            encryptor.update(save.encode()) + encryptor.finalize()
        )
        client_socket.send(f"Your save : {secure_save.decode()}\n".encode())

    def load_progress(self, client_socket, player_progress: dict):
        """
        Load player's progress
        """
        client_socket.send(b"\nEnter your encrypted save:\n> ")
        encrypted_save = client_socket.recv(1024)
        try:
            # Decode the base64
            decoded_save = base64.b64decode(encrypted_save)
            decryptor = self.cipher.decryptor()
            # Decrypt the save
            save = json.loads(
                decryptor.update(decoded_save) + decryptor.finalize()
            )
            # Update player stats
            player_progress["total_games"] = int(save.get("total_games"))
            player_progress["wins"] = int(save.get("wins"))
            player_progress["losses"] = int(save.get("losses"))
            player_progress["draws"] = int(save.get("draws"))
            player_progress["winrate"] = float(save.get("winrate"))

            client_socket.send(b"\nYour stats have been upgraded!\n")
        except:
            client_socket.send(b"\nError during decryption!\n")

    def show_flag(self, client_socket, player_progress):
        """
        Show the secret flag
        """
        # Players needs to win 100 games in a row to retrieve flag. Good luck!
        if player_progress["total_games"] >= 100 and player_progress["winrate"] == 100.0:
            client_socket.send(b"\nCongratulations! You're the master of Rock-Paper-Scissors!\n")
            client_socket.send(f"The flag is : {FLAG}\n".encode())
        else:
            client_socket.send(b"Sorry, the secret belong to the master...\n")


class RockPaperScissorsServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


# Entry point
if __name__ == "__main__":
    # Default logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger("RockPaperScissors")

    HOST = '0.0.0.0'
    PORT = 5000

    server = RockPaperScissorsServer((HOST, PORT), RockPaperScissors)
    logger.info(f"Start listening on [{HOST}:{PORT}]")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")

