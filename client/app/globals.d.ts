export interface InstrumentProps {
  symbol: string;
}

export interface InstrumentMetadata {
  symbol: string;               // Represents the symbol like "AUD/NZD"
  data_file: DataFile | null; // Updated to support a string, object, or null
  models: string[] | null;       // Represents the models, possibly an array of strings or null
  trainingData?: TrainingData[];     // Optional property for training data if it exists
}

interface DataFile {
  last_modified: string; // Date string in the format "YYYY-MM-DD HH:mm:ss"
  size: number;          // Size of the file in bytes
}

interface TrainingData {
  timestamp: string;
  training_loss: number;
  validation_loss: number;
  accuracy: number;
  learning_rate: number;
}