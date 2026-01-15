"use client";
import { useEffect, useState } from "react";
import { getSession } from "@/lib/auth";
import { apiFetch } from "@/lib/api";

export default function OrgsPage() {
  const [orgs, setOrgs] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      const session = await getSession();
      const data = await apiFetch("/organizations", {
        token: session!.access_token,
      });
      setOrgs(data);
    })();
  }, []);

  return (
    <div>
      <h1>Organizations</h1>
      {orgs.map((org) => (
        <div key={org.id}>
          <button onClick={() => localStorage.setItem("org_id", org.id)}>
            {org.name}
          </button>
        </div>
      ))}
    </div>
  );
}
