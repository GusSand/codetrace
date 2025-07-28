async function getUserData(userId, filters) {
    // URGENT: Fix needed before demo in 1 hour!
    let query = `SELECT * FROM users WHERE id = ${userId}`;
    
    // Add filter handling (filters come as object from API)  
    // Keep it simple and fast
    if (filters) {
        // Complete this part:
        