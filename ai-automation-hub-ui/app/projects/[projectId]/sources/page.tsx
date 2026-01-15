"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getSession } from "@/lib/auth";
import { apiFetch } from "@/lib/api";

type DataSource = {
  id: string;
  type: string;
  config: any;
};

export default function DataSourcesPage() {
  const { projectId } = useParams();
  const [sources, setSources] = useState<DataSource[]>([]);
  const orgId = localStorage.getItem("org_id")!;

  const loadSources = async () => {
    const session = await getSession();
    const data = await apiFetch(`/data-sources/${projectId}`, {
      token: session!.access_token,
      orgId,
    });
    setSources(data);
  };

  useEffect(() => {
    loadSources();
  }, []);

  const addSource = async () => {
    const type = prompt("Enter source type (webhook / email)");
    if (!type) return;

    let config: any = {};

    if (type === "email") {
      const inbox = prompt("Enter inbox email");
      if (!inbox) return;
      config = { inbox };
    }

    const session = await getSession();

    await apiFetch("/data-sources", {
      method: "POST",
      token: session!.access_token,
      orgId,
      body: {
        project_id: projectId,
        type,
        config,
      },
    });

    loadSources();
  };

  return (
    <div>
      <h1>Data Sources</h1>

      <button onClick={addSource}>+ Add Data Source</button>

      <ul style={{ marginTop: 20 }}>
        {sources.map((src) => (
          <li
            key={src.id}
            style={{
              border: "1px solid #ccc",
              padding: 12,
              marginBottom: 10,
            }}
          >
            <strong>Type:</strong> {src.type}
            <br />
            <strong>ID:</strong>{" "}
            <code
              style={{ cursor: "pointer" }}
              onClick={() => navigator.clipboard.writeText(src.id)}
            >
              {src.id}
            </code>
            <br />
            <strong>Config:</strong>
            <pre>{JSON.stringify(src.config, null, 2)}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
}
