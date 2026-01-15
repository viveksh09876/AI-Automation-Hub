export async function apiFetch(
  path: string,
  {
    token,
    orgId,
    method = "GET",
    body,
  }: {
    token: string;
    orgId?: string;
    method?: string;
    body?: any;
  }
) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(orgId ? { "X-Org-Id": orgId } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) throw new Error("API error");
  return res.json();
}
