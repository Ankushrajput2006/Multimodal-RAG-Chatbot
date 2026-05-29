"""Document Upload component."""
import React, { useRef, useState } from "react";
import { useDocuments } from "../hooks/useDocuments";
import "../styles/DocumentUpload.css";

const DocumentUpload: React.FC = () => {
  const { uploading, uploadError, uploadDocument } = useDocuments();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});

  const handleFiles = async (files: FileList) => {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      try {
        setUploadProgress((prev) => ({ ...prev, [file.name]: 0 }));
        const result = await uploadDocument(file);
        setUploadProgress((prev) => ({ ...prev, [file.name]: 100 }));
        
        // Show success notification
        console.log(`✅ ${file.name}: ${result.chunks_added} chunks added`);
      } catch (error) {
        console.error(`Error uploading ${file.name}:`, error);
      }
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  return (
    <div className="document-upload">
      <div
        className={`upload-zone ${dragActive ? "active" : ""}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
          accept=".pdf,.txt,.jpg,.jpeg,.png,.gif"
          style={{ display: "none" }}
          disabled={uploading}
        />

        <div className="upload-content">
          <span className="upload-icon">📁</span>
          <p>Drag & drop documents or click to upload</p>
          <p className="upload-formats">PDF, TXT, JPG, PNG, GIF</p>
        </div>
      </div>

      {uploadError && <div className="upload-error">{uploadError}</div>}

      <div className="upload-progress">
        {Object.entries(uploadProgress).map(([fileName, progress]) => (
          <div key={fileName} className="progress-item">
            <span>{fileName}</span>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentUpload;
