
const total_users = 0;
const active_mentors = 0;
const active_mentees = 0;
const total_sessions = 0;
const completed_sessions = 0;
const total_feedback = 0;
const average_rating = 0;

const ctx = document.getElementById('analyticsChart').getContext('2d');
const analyticsChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [
      'Total Users',
      'Mentors',
      'Mentees',
      'Total Sessions',
      'Completed Sessions',
      'Total Feedback',
      'Average Rating'
    ],
    datasets: [{
      label: 'Analytics',
      data: [
        total_users,
        active_mentors,
        active_mentees,
        total_sessions,
        completed_sessions,
        total_feedback,
        average_rating
      ],
      backgroundColor: [
        '#007bff',
        '#198754',
        '#0dcaf0',
        '#ffc107',
        '#6c757d',
        '#adb5bd',
        '#343a40'
      ],
      borderColor: '#fff',
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: { beginAtZero: true }
    }
  }
});
