.model small
.stack 100h

.data
    msg db 'Hello, World!$'

.code
main:
    ; Inițializare segment de date
    mov ax, @data
    mov ds, ax

    ; Afișează mesajul
    mov ah, 09h       ; Funcția 09h - Afișează un mesaj
    lea dx, msg       ; Adresa mesajului
    int 21h           ; Apel întrerupere DOS

    ; Închide programul
    mov ah, 4Ch       ; Funcția 4Ch - Termină programul
    int 21h           ; Apel întrerupere DOS
end main