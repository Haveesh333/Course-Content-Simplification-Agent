export interface DifficultTerm {
  term: string;
  meaning: string;
}

export interface QuizQuestion {
  question: string;
  options: string[]; // 4 items: "A. ...", "B. ...", "C. ...", "D. ..."
  answer: string;    // "A" | "B" | "C" | "D"
}

export interface SimplifyResult {
  simplified_explanation: string;
  key_points: string[];
  difficult_terms: DifficultTerm[];
  examples: string[];
  quiz: QuizQuestion[];
}
