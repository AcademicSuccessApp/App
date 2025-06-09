import express from 'express';
import cors from 'cors';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 5173;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'dist')));

app.post('/api/predict', async (req, res) => {
  try {
    const { sem1, sem2, sem3, sem4, gender, programStudi } = req.body;
    
    // Log the received data
    console.log('Received prediction request with data:', {
      sem1, sem2, sem3, sem4, gender, programStudi
    });

    // Validate input data
    if (!sem1 || !sem2 || !sem3 || !sem4 || !gender || !programStudi) {
      console.error('Missing required fields:', { sem1, sem2, sem3, sem4, gender, programStudi });
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Spawn Python process
    const pythonProcess = spawn('python', [
      'predict.py',
      sem1,
      sem2,
      sem3,
      sem4,
      gender,
      programStudi
    ]);

    let predictionResult = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      predictionResult += data.toString();
      console.log('Python stdout:', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
      console.error('Python stderr:', data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`);
        console.error('Error output:', errorOutput);
        return res.status(500).json({ 
          error: 'Prediction failed',
          details: errorOutput
        });
      }

      try {
        console.log('Raw prediction result:', predictionResult);
        const result = JSON.parse(predictionResult);
        res.json(result);
      } catch (error) {
        console.error('Failed to parse prediction result:', error);
        console.error('Raw prediction result:', predictionResult);
        res.status(500).json({ 
          error: 'Invalid prediction result',
          details: error.message,
          rawResult: predictionResult
        });
      }
    });
  } catch (error) {
    console.error('Prediction error:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      details: error.message
    });
  }
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}); 