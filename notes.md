Long term objectives have the followin attributes: 
  title: String;                   // Concise, clear name of the objective (e.g., "Become Market Leader in Sustainable Packaging by 2028")
  description: String;             // Detailed explanation of what the objective entails, its purpose, and scope.
  level: Enum;                     // E.g., "ORGANIZATIONAL", "DEPARTMENTAL", "TEAM", "INDIVIDUAL"
  ownerId: int      // Owner team memeber
  parentObjectiveId: int  (nullable); // ID of the objective this one directly supports (for cascading/hierarchy)
  status: Enum;                    // E.g., "NOT_STARTED", "ON_TRACK", "AT_RISK", "DELAYED", "ACHIEVED", "ON_HOLD", "CANCELLED"
  priority: Enum (nullable);       // E.g., "HIGH", "MEDIUM", "LOW"
  startDate: Date;                 // Planned start date for working on the objective
  targetCompletionDate: Date;      // Planned end date or deadline for the objective
  actualCompletionDate: Date (nullable); // Actual date the objective was achieved
  creationDate: DateTime;          // When the objective was created
  lastUpdatedDate: DateTime;       // When the objective was last modified
  alignmentStatement: String (nullable); // Brief explanation of how this objective aligns with broader goals or parent objectives
  tags: Array<String> (nullable);  // Keywords for categorization or filtering (e.g., "Innovation", "EMEA_Market", "Sustainability")
  confidentiality: Enum (nullable); // E.g., "PUBLIC", "INTERNAL", "RESTRICTED"
  strategicPerspective: Enum (nullable); // E.g., "FINANCIAL", "CUSTOMER", "INTERNAL_PROCESS", "LEARNING_GROWTH"
  progressUpdates: Array<ProgressUpdate> (nullable); // Log of updates, comments, and progress notes
  reviewCadence: Enum (nullable);  // E.g., "MONTHLY", "QUARTERLY", "BI_ANNUALLY", "ANNUALLY"
  lastReviewDate: Date (nullable);
