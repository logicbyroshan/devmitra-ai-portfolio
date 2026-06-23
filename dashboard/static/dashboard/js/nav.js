// nav.js (No changes needed)

// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    
    // Find the element where the date will be displayed
    const dateElement = document.getElementById('current-date');
    
    // Check if the element exists to avoid errors
    if (dateElement) {
        // Create a new Date object
        const today = new Date();
        
        // Define options for formatting the date
        const options = {
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        
        // Format the date according to the user's locale and the specified options
        const formattedDate = today.toLocaleDateString('en-US', options);
        
        // Set the text content of the element to the formatted date
        dateElement.textContent = formattedDate;
    }

});