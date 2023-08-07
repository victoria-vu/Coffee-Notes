'use strict';

const addNotesButtons = document.querySelectorAll('.show-textbox');
const forms = document.querySelectorAll('.notes-textbox');
const closeNotesButtons = document.querySelectorAll('.close-textbox');

// Hides all forms
if (forms) {
    for (const form of forms) { 
        form.hidden = true;
    }
};

// Show Notes Textbox
if (addNotesButtons) {
    for (const addNoteButton of addNotesButtons) {
        addNoteButton.addEventListener('click', () => {
            const formID = addNoteButton.id.replace('show', 'notes');
            const form = document.querySelector(`#${formID}`);

            form.hidden = false;
        })
    }
};

// Close Notes Textbox
if (closeNotesButtons) {
    for (const closeNoteButton of closeNotesButtons) {
        closeNoteButton.addEventListener('click', () => {
            const formID = closeNoteButton.id.replace('close', 'notes');
            const form = document.querySelector(`#${formID}`);

            form.hidden = true;
        })
    }
};