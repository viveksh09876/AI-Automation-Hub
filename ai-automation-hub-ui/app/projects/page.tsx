"use client";

import { useEffect, useState } from "react";
import { getSession } from "@/lib/auth";
import { apiFetch } from "@/lib/api";

type Project = {
  id: string;
  name: string;
  type: string;
};

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const orgId = localStorage.getItem("org_id")!;

  const loadProjects = async () => {
    const session = await getSession();
    const data = await apiFetch("/projects", {
      token: session!.access_token,
      orgId,
    });
    setProjects(data);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const createProject = async () => {
    const name = prompt("Project name");
    if (!name) return;

    const type =
      prompt("Project type (email_ai / support_ai / sales_ai)") ?? "email_ai";

    const session = await getSession();

    await apiFetch("/projects", {
      method: "POST",
      token: session!.access_token,
      orgId,
      body: { name, type },
    });

    loadProjects();
  };

  return (
    <div>
      <h1>Projects</h1>

      <button onClick={createProject}>+ Create Project</button>

      <ul style={{ marginTop: 20 }}>
        {projects.map((p) => (
          <li key={p.id}>
            <a href={`/projects/${p.id}/files`}>
              {p.name} ({p.type})
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
