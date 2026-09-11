import { useState } from "react";
import axios from "axios";
import { SimplifyResult } from "../types";

interface UseSimplifyReturn {
  simplify: (file: File | null, text: string, level: string) => Promise<void>;
  data: SimplifyResult | null;
  loading: boolean;
  error: string | null;
}

export function useSimplify(): UseSimplifyReturn {
  const [data, setData] = useState<SimplifyResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const simplify = async (
    file: File | null,
    text: string,
    level: string
  ): Promise<void> => {
    setLoading(true);
    setError(null);
    setData(null);

    const formData = new FormData();
    if (file !== null) {
      formData.append("file", file);
    }
    if (text !== "") {
      formData.append("text", text);
    }
    formData.append("level", level);

    try {
      const response = await axios.post<SimplifyResult>(
        "/api/simplify",
        formData
      );
      setData(response.data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  return { simplify, data, loading, error };
}
