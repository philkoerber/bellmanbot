export interface InstrumentProps {
  symbol: string;
}

export interface InstrumentMetadata {
  symbol: string;               // Represents the symbol like "AUD/NZD"
  data_file: DataFile | null;  // Represents metadata about the data file or null if not available
  results?: TrainingResults | null; // Represents training results or null if not available
}

interface DataFile {
  last_modified: string; // Date string in the format "YYYY-MM-DD HH:mm:ss"
  size: number;          // Size of the file in bytes
}

interface TrainingResults {
  loss: number;         // Latest training loss value
  accuracy?: number;    // Optional field for accuracy if available
  val_loss?: number;    // Optional field for validation loss if available
  val_accuracy?: number; // Optional field for validation accuracy if available
}
