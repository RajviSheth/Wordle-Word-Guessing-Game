# Wordle-Word-Guessing-Game
Welcome to the Wordle Word Guessing Game! 

This repository contains the implementation of the popular game Wordle using *Python* and *Pandas*, where players attempt to guess a five-letter word within six attempts.

The Wordle game in this repository incorporates an intelligent word suggestion feature that recommends the best first word to guess based on statistical analysis. As the game progresses and the player provides feedback on the letters and their positions, the program generates and suggests the most suitable next word for guessing. This process is followed till the final word is guessed correctly!

## Features

- Intelligent word suggestion: The program suggests the best first word to guess based on statistical analysis of common English words and the alphabet frequencies.
- Method: -- Calculates the probabilities of all the letters and vowels from the words list.
          -- Uses the concept of the Lavenstein distance, which basically looks at the difference/distance between 2 words.
- Progressive word suggestions: As the player provides feedback on the letters and their positions, the program dynamically generates subsequent word suggestions that match the given criteria.
- Limited attempts: The game allows a maximum of six attempts to guess the correct word.
