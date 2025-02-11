import { useState } from "react";
import {
  Container,
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  CircularProgress,
} from "@mui/material";
import { askQuestion } from "@services/api";
import type { QuestionResponse } from "@/types/api";
import ReactMarkdown from "react-markdown";
import { QAService } from "@services/qa/qaService";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<QuestionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await QAService.askQuestion({ 
        text: question,
        n_results: 5 
      });
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Turkish Legal AI Assistant
      </Typography>

      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <TextField
          fullWidth
          label="Ask a question about Turkish Criminal Law"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          multiline
          rows={3}
          variant="outlined"
          sx={{ mb: 2 }}
        />
        <Button
          type="submit"
          variant="contained"
          disabled={loading || !question.trim()}
          sx={{ minWidth: 120 }}
        >
          {loading ? <CircularProgress size={24} /> : "Ask"}
        </Button>
      </Box>

      {error && (
        <Paper
          sx={{
            p: 2,
            mb: 2,
            bgcolor: "error.light",
            color: "error.contrastText",
          }}
        >
          <Typography>{error}</Typography>
        </Paper>
      )}

      {response && (
        <Box>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Answer
            </Typography>
            <ReactMarkdown>{response.answer}</ReactMarkdown>
            {response.confidence_score && (
              <Typography variant="body2" color="text.secondary">
                Confidence Score: {(response.confidence_score * 100).toFixed(1)}
                %
              </Typography>
            )}
            <Typography variant="body2" color="text.secondary">
              Processing Time: {response.processing_time.toFixed(2)}s
            </Typography>
          </Paper>

          <Typography variant="h6" gutterBottom>
            Sources
          </Typography>
          {response.sources.map((source) => (
            <Paper key={source.id} sx={{ p: 2, mb: 2 }}>
              <Typography variant="body1">{source.content}</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {Object.entries(source.metadata)
                  .map(([key, value]) => `${key}: ${value}`)
                  .join(" | ")}
              </Typography>
            </Paper>
          ))}
        </Box>
      )}
    </Container>
  );
}

export default App;
