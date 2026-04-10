// Dashboard JavaScript functionality

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
    updateCurrentDate();
});

// Initialize dashboard components
function initializeDashboard() {
    // Check if user is logged in
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser || currentUser.role !== 'admin') {
        window.location.href = 'login.html';
        return;
    }

    // Update user welcome message
    document.getElementById('current-user').textContent = `Welcome, ${currentUser.username}`;

    // Load initial data
    loadDashboardData();
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const section = item.getAttribute('data-section');
            switchSection(section);
        });
    });

    // Logout button
    document.getElementById('logout-btn').addEventListener('click', logout);

    // Form submissions
    document.getElementById('add-user-form')?.addEventListener('submit', handleAddUser);
    document.getElementById('action-form')?.addEventListener('submit', handleActionSubmit);

    // Close modals on outside click
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                closeModal(modal.id);
            }
        });
    });
}

// Switch between sections
function switchSection(sectionId) {
    // Update navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-section') === sectionId) {
            item.classList.add('active');
        }
    });

    // Update content
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
        if (section.id === sectionId) {
            section.classList.add('active');
        }
    });

    // Update title
    const titleMap = {
        'dashboard': 'Admin Dashboard',
        'user-management': 'User Management',
        'disease-verification': 'Disease Verification',
        'schedule-management': 'Schedule Management',
        'complaint-handling': 'Complaint Handling',
        'report-submission': 'Report Submission'
    };
    
    document.getElementById('section-title').textContent = titleMap[sectionId] || 'Admin Dashboard';

    // Load section-specific data
    switch(sectionId) {
        case 'user-management':
            loadUsers();
            break;
        case 'disease-verification':
            loadDiseaseReports();
            break;
        case 'schedule-management':
            loadSchedules();
            break;
        case 'complaint-handling':
            loadComplaints();
            break;
    }
}

// Update current date
function updateCurrentDate() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    document.getElementById('current-date').textContent = now.toLocaleDateString('en-US', options);
}

// Load dashboard data
function loadDashboardData() {
    // Simulate loading data
    setTimeout(() => {
        // This would typically be API calls in a real application
        console.log('Dashboard data loaded');
    }, 500);
}

// User Management Functions
function loadUsers() {
    // Simulate loading users from API
    console.log('Loading users...');
}

function showAddUserModal() {
    document.getElementById('add-user-modal').style.display = 'block';
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        // Simulate API call to delete user
        console.log(`Deleting user ${userId}`);
        alert('User deleted successfully');
        // Refresh user list
        loadUsers();
    }
}

function handleAddUser(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const userData = {
        name: formData.get('name'),
        email: formData.get('email'),
        role: formData.get('role')
    };
    
    // Simulate API call to add user
    console.log('Adding user:', userData);
    alert('User added successfully');
    closeModal('add-user-modal');
    event.target.reset();
    loadUsers();
}

// Disease Verification Functions
function loadDiseaseReports() {
    // Simulate loading disease reports
    console.log('Loading disease reports...');
}

function verifyReport(reportId) {
    if (confirm('Verify this disease report?')) {
        // Simulate API call to verify report
        console.log(`Verifying report ${reportId}`);
        alert('Report verified successfully');
        loadDiseaseReports();
    }
}

function deleteReport(reportId) {
    if (confirm('Delete this disease report?')) {
        // Simulate API call to delete report
        console.log(`Deleting report ${reportId}`);
        alert('Report deleted successfully');
        loadDiseaseReports();
    }
}

// Schedule Management Functions
function loadSchedules() {
    // Simulate loading schedules
    console.log('Loading schedules...');
}

function showScheduleModal() {
    // Implement schedule modal
    alert('Schedule modal would open here');
}

// Complaint Handling Functions
function loadComplaints() {
    // Simulate loading complaints
    console.log('Loading complaints...');
}

function acceptComplaint(complaintId) {
    showActionModal(complaintId, 'accept');
}

function rejectComplaint(complaintId) {
    if (confirm('Reject this complaint?')) {
        // Simulate API call to reject complaint
        console.log(`Rejecting complaint ${complaintId}`);
        alert('Complaint rejected');
        loadComplaints();
    }
}

function showActionModal(complaintId, action) {
    document.getElementById('action-modal').style.display = 'block';
    // Store current complaint ID for form submission
    document.getElementById('action-modal').dataset.complaintId = complaintId;
    document.getElementById('action-modal').dataset.action = action;
}

function handleActionSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const actionData = {
        description: formData.get('description'),
        priority: formData.get('priority'),
        complaintId: event.target.closest('.modal').dataset.complaintId,
        action: event.target.closest('.modal').dataset.action
    };
    
    // Simulate API call
    console.log('Submitting action:', actionData);
    alert('Action submitted successfully');
    closeModal('action-modal');
    event.target.reset();
    loadComplaints();
}

// Modal Functions
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Logout function
function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}

// Utility functions
function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        background: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        border-radius: 4px;
        z-index: 3000;
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Simulated data (would be replaced with actual API calls)
const mockData = {
    users: [
        { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Health Worker', status: 'active' },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'Citizen', status: 'active' },
        { id: 3, name: 'Mike Johnson', email: 'mike@example.com', role: 'Health Worker', status: 'inactive' }
    ],
    reports: [
        { id: 1, title: 'Malaria Outbreak - Area 3', reporter: 'Citizen #123', date: '2024-01-15' },
        { id: 2, title: 'Dengue Suspected - Area 7', reporter: 'Health Worker #45', date: '2024-01-14' }
    ],
    complaints: [
        { id: 1, title: 'Water Quality Issue - Area 4', submitter: 'Citizen #789', date: '2024-01-13' },
        { id: 2, title: 'Garbage Collection - Area 6', submitter: 'Citizen #456', date: '2024-01-12' }
    ]
};

// Export functions for global access
window.showAddUserModal = showAddUserModal;
window.deleteUser = deleteUser;
window.verifyReport = verifyReport;
window.deleteReport = deleteReport;
window.showScheduleModal = showScheduleModal;
window.acceptComplaint = acceptComplaint;
window.rejectComplaint = rejectComplaint;
window.closeModal = closeModal;
