function deleteNote(noteId) {
  // Send a POST request to the server to delete the note
  fetch("/delete-note", {
      method: "POST",  // HTTP method
      body: JSON.stringify({ noteId: noteId }),  // Convert noteId to JSON and send it as the request body
  }).then((_res) => {
      // After the request is completed, redirect to the home page
      window.location.href = "/";
  });
}