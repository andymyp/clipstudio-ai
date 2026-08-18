type PlaceholderPageProps = { title: string };

export function PlaceholderPage({ title }: PlaceholderPageProps) {
  return (
    <section>
      <p className="eyebrow">APPLICATION MODULE</p>
      <h1>{title}</h1>
      <p className="muted">This navigation surface is reserved for its implementation prompt.</p>
    </section>
  );
}
