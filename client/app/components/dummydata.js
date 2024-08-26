const trainingLossData = [
  { x: 1, y: 0.8 },
  { x: 2, y: 0.6 },
  { x: 3, y: 0.4 },
  { x: 4, y: 0.35 },
  { x: 5, y: 0.3 },
  { x: 6, y: 0.28 },
  { x: 7, y: 0.26 },
  { x: 8, y: 0.24 },
  { x: 9, y: 0.22 },
  { x: 10, y: 0.2 }
];

const validationLossData = [
  { x: 1, y: 0.9 },
  { x: 2, y: 0.7 },
  { x: 3, y: 0.5 },
  { x: 4, y: 0.45 },
  { x: 5, y: 0.4 },
  { x: 6, y: 0.38 },
  { x: 7, y: 0.36 },
  { x: 8, y: 0.34 },
  { x: 9, y: 0.32 },
  { x: 10, y: 0.3 }
];

export const chartData = [
  {
      id: 'Training Loss',
      data: trainingLossData,
  },
  {
      id: 'Validation Loss',
      data: validationLossData,
  }
];