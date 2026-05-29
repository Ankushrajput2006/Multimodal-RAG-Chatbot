"""Hook for managing document uploads."""
import { useState, useCallback } from "react";
import apiClient from "../utils/apiClient";
import * as Types from "../types/api";

export const useDocuments = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const uploadDocument = useCallback(async (file: File) => {
    setUploading(true);
    setUploadError(null);

    try {
      const response = await apiClient.uploadDocument(file);
      return response;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Upload failed";
      setUploadError(errorMessage);
      throw err;
    } finally {
      setUploading(false);
    }
  }, []);

  return {
    uploading,
    uploadError,
    uploadDocument,
  };
};
