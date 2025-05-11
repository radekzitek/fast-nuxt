KeyResult {
  keyResultId: String;             // Unique identifier for the key result
  objectiveId: String;             // Foreign key linking back to the parent Objective
  description: String;             // What will be measured (e.g., "Increase customer retention rate")
  targetValue: Number;             // The desired value to achieve (e.g., 85 for 85%)
  currentValue: Number;            // The current value of the metric
  startValue: Number (nullable);   // The value at the beginning of tracking this KR
  unit: String;                    // Unit of measurement (e.g., "%", "USD", "Number", "NPS Score")
  status: Enum;                    // E.g., "NOT_STARTED", "ON_TRACK", "AT_RISK", "ACHIEVED", "CLOSED"
  dueDate: Date (nullable);        // Specific due date for this KR, if different from objective's
  ownerId: String (nullable);      // Specific owner for this KR, if different from objective owner
  confidenceLevel: Enum (nullable); // E.g. (for OKRs): "HIGH_CONFIDENCE", "MEDIUM_CONFIDENCE", "LOW_CONFIDENCE"
  complexity: Enum;                 // "LOW", "MEDIUM", "HIGH"
