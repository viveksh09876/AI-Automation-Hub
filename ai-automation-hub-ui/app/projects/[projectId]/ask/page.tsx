"use client";
import { useState } from "react";
import { useParams } from "next/navigation";
import { getSession } from "@/lib/auth";
import { apiFetch } from "@/lib/api";

export default function AskPage() {
  const { projectId } = useParams();
  const [q, setQ] = useState("");
  const [a, setA] = useState("");
  const orgId = localStorage.getItem("org_id")!;

  const ask = async () => {
    const session = await getSession();
    const res = await apiFetch(`/qa/${projectId}`, {
      method: "POST",
      token: session!.access_token,
      orgId,
      body: { question: q },
    });
    setA(res.answer);
  };

  return (
    <div>
      <h1>Ask Knowledge Base</h1>
      <input value={q} onChange={(e) => setQ(e.target.value)} />
      <button onClick={ask}>Ask</button>
      <p>{a}</p>
    </div>
  );
}
