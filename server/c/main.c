#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// Hash table for storing dictionary words
#define TABLE_SIZE 1000000
#define MAX_WORD_LENGTH 100

typedef struct HashNode {
    char* word;
    struct HashNode* next;
} HashNode;

HashNode* hash_table[TABLE_SIZE];

// Simple hash function to hash words
unsigned int hash(char* word) {
    unsigned int hash_value = 0;
    while (*word) {
        hash_value = (hash_value * 31) + *word++;
    }
    return hash_value % TABLE_SIZE;
}

// Insert a word into the hash table
void insert_word(const char* word) {
    unsigned int index = hash(word);
    HashNode* new_node = (HashNode*)malloc(sizeof(HashNode));
    new_node->word = strdup(word);
    new_node->next = hash_table[index];
    hash_table[index] = new_node;
}

// Search for a word in the hash table
bool search_word(const char* word) {
    unsigned int index = hash(word);
    HashNode* current = hash_table[index];
    while (current) {
        if (strcmp(current->word, word) == 0) {
            return true;
        }
        current = current->next;
    }
    return false;
}

// Load the dictionary into the hash table
void load_dictionary(const char* dictionary_file) {
    FILE* file = fopen(dictionary_file, "r");
    if (file == NULL) {
        printf("Error: Could not open dictionary file.\n");
        exit(1);
    }

    char word[MAX_WORD_LENGTH];
    while (fscanf(file, "%s", word) != EOF) {
        insert_word(word);
    }

    fclose(file);
}

// Free memory used by the hash table
void free_hash_table() {
    for (int i = 0; i < TABLE_SIZE; i++) {
        HashNode* current = hash_table[i];
        while (current) {
            HashNode* temp = current;
            current = current->next;
            free(temp->word);
            free(temp);
        }
    }
}

// Function to generate permutations of a specific word length
void permute(char* letters, int* used, char* current_word, int current_index, int word_length, int* result_count) {
    // Base case: if the current index is equal to the word length, check if it's a valid word
    if (current_index == word_length) {
        current_word[current_index] = '\0'; // Null-terminate the string
        if (search_word(current_word)) {
            printf("%s\n", current_word);
            (*result_count)++;
        }
        return;
    }

    // Try every letter in the letters array and recurse
    for (int i = 0; i < strlen(letters); i++) {
        if (!used[i]) { // If the letter has not been used yet
            used[i] = 1; // Mark the letter as used
            current_word[current_index] = letters[i]; // Choose the letter
            permute(letters, used, current_word, current_index + 1, word_length, result_count);
            used[i] = 0; // Backtrack: Unmark the letter
        }
    }
}

// Function to find words of all specified lengths
void find_words(char* letters, int* lengths, int num_lengths) {
    int result_count = 0;

    // For each length in the lengths array
    for (int i = 0; i < num_lengths; i++) {
        int word_length = lengths[i];

        // Skip lengths larger than the number of available letters
        if (word_length > strlen(letters)) {
            printf("Cannot generate words of length %d (not enough letters)\n", word_length);
            continue;
        }

        printf("Words of length %d:\n", word_length);

        // Create an array to track used letters
        int* used = (int*)malloc(strlen(letters) * sizeof(int));
        for (int j = 0; j < strlen(letters); j++) {
            used[j] = 0; // Initially, no letters are used
        }

        // Create a buffer for the current word being formed
        char* current_word = (char*)malloc((word_length + 1) * sizeof(char));
        current_word[word_length] = '\0'; // Null-terminate the string

        // Generate all permutations for the given word length
        permute(letters, used, current_word, 0, word_length, &result_count);

        free(used); // Clean up the used array
        free(current_word); // Clean up the current word buffer
    }

    printf("\nTotal valid words generated: %d\n", result_count);
}

int main(int argc, char *argv[]) {
    // Check if sufficient arguments are passed
    if (argc < 3) {
        printf("Usage: %s <letters> <lengths> <dictionary_file>\n", argv[0]);
        return 1;
    }

    // Get the letters and lengths as input
    char* letters_str = argv[1];
    char* lengths_str = argv[2];
    char* dictionary_file = argv[3];

    // Load the dictionary
    load_dictionary(dictionary_file);

    // Initialize pointers and counters
    int letter_count = 0;
    int lengths_count = 0;

    // Count the number of letters (comma separated) in letters_str
    char* temp = strdup(letters_str); // Make a copy of the string
    char* token = strtok(temp, ",");
    while (token != NULL) {
        letter_count++;
        token = strtok(NULL, ",");
    }
    free(temp); // Clean up

    // Count the number of lengths (comma separated) in lengths_str
    temp = strdup(lengths_str);
    token = strtok(temp, ",");
    while (token != NULL) {
        lengths_count++;
        token = strtok(NULL, ",");
    }
    free(temp); // Clean up

    // Parse the lengths array from the string of lengths
    int* lengths = (int*)malloc(lengths_count * sizeof(int));
    if (lengths == NULL) {
        printf("Memory allocation failed for lengths!\n");
        return 1;
    }

    // Parse the letters array from the string of letters
    char* letters = (char*)malloc(letter_count * sizeof(char));
    if (letters == NULL) {
        printf("Memory allocation failed for letters!\n");
        return 1;
    }

    // Split the letters string into individual characters using strtok
    token = strtok(letters_str, ",");
    int i = 0;
    while (token != NULL && i < letter_count) {
        letters[i] = token[0]; // Take the first character of the token
        token = strtok(NULL, ",");
        i++;
    }

    // Split the lengths string into integers using a comma delimiter
    token = strtok(lengths_str, ",");
    i = 0;
    while (token != NULL && i < lengths_count) {
        lengths[i] = atoi(token);  // Convert string to integer
        token = strtok(NULL, ",");
        i++;
    }

    // Find all possible valid words
    find_words(letters, lengths, lengths_count);

    // Clean up dynamically allocated memory
    free(lengths);
    free(letters);

    // Free the dictionary hash table
    free_hash_table();

    return 0;
}

