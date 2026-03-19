import React, { useState } from 'react';
import { MOCK_TASKS } from '../mockData';

const PHASES = [
  { phase: 1, name: 'Critical Assets', timeline: 'Apr–Jul 2026', start: 0, width: 33, color: '#ef4444' },
  { phase: 2, name: 'High Priority', timeline: 'Aug–Oct 2026', start: 33, width: 25, color: '#f97316' },
  { phase: 3, name: 'Remaining', timeline: 'Nov 2026–Jan 2027', start: 58, width: 25, color: '#eab308' },
];

const prioColors = { critical: '#ef4444', high: '#f97316', medium: '#eab308', low: '#22c55e' };

export default function Remediation() {
  const [view, setView] = useState('kanban');
  const pending = MOCK_TASKS.filter(t => t.status === 'pending');
  const inProgress = MOCK_TASKS.filter(t => t.status === 'in_progress');
  const completed = MOCK_TASKS.filter(t => t.status === 'completed');

  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div>
          <h1 className="page-title">Remediation Hub</h1>
          <p className="page-subtitle">PQC migration orchestration — 9-month roadmap to quantum safety</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className={`btn ${view === 'kanban' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setView('kanban')}>Kanban</button>
          <button className={`btn ${view === 'gantt' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setView('gantt')}>Gantt</button>
        </div>
      </div>

      {view === 'kanban' ? (
        <div className="kanban-board">
          <KanbanColumn title="⏳ Pending" tasks={pending} color="var(--score-moderate)" />
          <KanbanColumn title="🔄 In Progress" tasks={inProgress} color="var(--accent-primary)" />
          <KanbanColumn title="✅ Completed" tasks={completed} color="var(--score-safe)" />
        </div>
      ) : (
        <div className="card">
          <div className="card-header"><span className="card-title">9-Month Migration Roadmap</span></div>
          <div style={{ display: 'flex', gap: 0, marginBottom: 16, fontSize: '0.7rem', color: 'var(--text-muted)' }}>
            {['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'].map((m, i) => (
              <div key={m} style={{ flex: 1, textAlign: 'center', padding: '6px 0', borderBottom: '1px solid var(--border-color)' }}>{m}</div>
            ))}
          </div>
          {MOCK_TASKS.map(task => {
            const phase = PHASES.find(p => p.phase === task.phase);
            return (
              <div className="gantt-row" key={task.taskId}>
                <div className="gantt-label" style={{ color: 'var(--text-secondary)' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 500 }}>{task.taskId}</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{task.assetId.split('.')[0]}</div>
                </div>
                <div className="gantt-bar-track">
                  <div className="gantt-bar" style={{ left: `${phase?.start || 0}%`, width: `${phase?.width || 20}%`, background: `${phase?.color || '#6366f1'}aa` }}>
                    {task.effortHours}h
                  </div>
                </div>
              </div>
            );
          })}
          <div style={{ marginTop: 16, display: 'flex', gap: 16, justifyContent: 'center' }}>
            {PHASES.map(p => (
              <div key={p.phase} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <span style={{ width: 12, height: 12, borderRadius: 3, background: p.color, display: 'inline-block' }} />
                Phase {p.phase}: {p.name}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function KanbanColumn({ title, tasks, color }) {
  return (
    <div className="kanban-column">
      <div className="kanban-column-header">
        <span className="kanban-column-title">{title}</span>
        <span className="kanban-count">{tasks.length}</span>
      </div>
      {tasks.map(task => (
        <div className="kanban-card" key={task.taskId}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{task.taskId}</span>
            <span className={`score-badge ${task.priority === 'critical' ? 'critical' : task.priority === 'high' ? 'high' : task.priority === 'medium' ? 'moderate' : 'safe'}`}>
              {task.priority}
            </span>
          </div>
          <div className="kanban-card-title">{task.title}</div>
          <div className="kanban-card-meta">
            <span>{task.assetId.split('.')[0]}</span>
            <span>{task.effortHours}h · Due {task.dueDate.slice(5)}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
