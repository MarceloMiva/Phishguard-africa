// src/app.ts

import express from 'express';
import { json } from 'body-parser';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(json());

// Routes (to be defined later)
// app.use('/api', apiRoutes);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

export default app;