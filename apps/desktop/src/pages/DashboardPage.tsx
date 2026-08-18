export function DashboardPage() {
  return (
    <section>
      <p className="eyebrow">LOCAL-FIRST CONTENT OPERATIONS</p>
      <h1>Production dashboard</h1>
      <p className="muted">
        The application shell is ready. Agents, workflows, and review queues arrive in later phases.
      </p>
      <div className="status-card">
        <span className="status-dot" />
        <div>
          <strong>Foundation online</strong>
          <p>Connect the backend to see live system status.</p>
        </div>
      </div>
    </section>
  );
}
