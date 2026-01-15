"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getSession } from "@/lib/auth";

type FileItem = {
  id: string;
  filename: string;
  status: string;
};

export default function FilesPage() {
  const { projectId } = useParams();
  const [files, setFiles] = useState<FileItem[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const orgId = localStorage.getItem("org_id")!;

  const loadFiles = async () => {
    const session = await getSession();

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/files/${projectId}`,
      {
        headers: {
          Authorization: `Bearer ${session!.access_token}`,
          "X-Org-Id": orgId,
        },
      }
    );

    setFiles(await res.json());
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const uploadFile = async () => {
    if (!file) return;

    const session = await getSession();
    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/files/${projectId}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session!.access_token}`,
        "X-Org-Id": orgId,
      },
      body: formData,
    });

    setFile(null);
    loadFiles();
  };

  return (
    <div>
      <h1>Files</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      <button onClick={uploadFile}>Upload</button>

      <ul style={{ marginTop: 20 }}>
        {files.map((f) => (
          <li key={f.id}>
            {f.filename} — <strong>{f.status}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}
