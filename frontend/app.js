// API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000';

// Get form elements
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loginContainer = document.getElementById('loginContainer');
const registerContainer = document.getElementById('registerContainer');
const interPage = document.getElementById('interPage');

// Add event listeners
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}

if (registerForm) {
    registerForm.addEventListener('submit', handleRegister);
}

// Toggle between login and register forms
function toggleForms() {
    if (loginContainer) {
        loginContainer.classList.toggle('hidden');
    }
    if (registerContainer) {
        registerContainer.classList.toggle('hidden');
    }
    clearMessages();
}

// Clear all messages
function clearMessages() {
    const loginMessage = document.getElementById('loginMessage');
    const registerMessage = document.getElementById('registerMessage');

    if (loginMessage) loginMessage.innerHTML = '';
    if (registerMessage) registerMessage.innerHTML = '';
}

// Show message
function showMessage(containerId, message, type) {
    const messageDiv = document.getElementById(containerId);
    if (!messageDiv) return;
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
}

// Handle Registration
async function handleRegister(e) {
    e.preventDefault();

    const fullname = document.getElementById('registerFullname').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const password2 = document.getElementById('registerPassword2').value;

    if (password !== password2) {
        showMessage('registerMessage', 'Passwords do not match', 'error');
        return;
    }

    if (password.length < 6) {
        showMessage('registerMessage', 'Password must be at least 6 characters', 'error');
        return;
    }

    showMessage('registerMessage', 'Registering...', 'loading');

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fullname,
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('registerMessage', 'Registration successful! Please login.', 'success');
            if (registerForm) registerForm.reset();
            setTimeout(() => {
                toggleForms();
                const loginEmail = document.getElementById('loginEmail');
                if (loginEmail) loginEmail.value = email;
            }, 2000);
        } else {
            showMessage('registerMessage', data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showMessage('registerMessage', 'Error: ' + error.message, 'error');
    }
}

// Handle Login
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    showMessage('loginMessage', 'Logging in...', 'loading');

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('email', email);

            const userId = await fetchUserIdByEmail(email);
            if (userId) {
                localStorage.setItem('userId', userId);
            }

            showMessage('loginMessage', 'Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = 'inter.html';
            }, 700);
        } else {
            showMessage('loginMessage', data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('loginMessage', 'Error: ' + error.message, 'error');
    }
}

async function fetchUserIdByEmail(email) {
    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        if (!response.ok) return null;

        const users = await response.json();
        const user = users.find(u => u.email?.toLowerCase() === email?.toLowerCase());
        return user?.id || null;
    } catch (error) {
        console.error('fetchUserIdByEmail error:', error);
        return null;
    }
}

async function loadDashboardData(userId, token) {
    await Promise.all([
        loadProgress(userId, token),
        loadWorkouts(userId, token),
        loadNutrition(userId, token)
    ]);
}

async function loadProgress(userId, token) {
    const progressList = document.getElementById('progressList');
    if (!progressList) return;

    try {
        const response = await fetch(`${API_BASE_URL}/progress/user/${userId}`, {
            headers: buildHeaders(token)
        });
        const progress = response.ok ? await response.json() : [];

        progressList.innerHTML = progress.length
            ? progress.map(item => renderProgressItem(item)).join('')
            : '<p>No progress entries yet. Add one below.</p>';
    } catch (error) {
        console.error('loadProgress error:', error);
        progressList.innerHTML = '<p>Unable to load progress.</p>';
    }
}

function renderProgressItem(item) {
    return `
        <div class="item-card">
            <strong>Weight:</strong> ${item.weight} kg<br>
            <strong>Height:</strong> ${item.height} m<br>
            <strong>BMI:</strong> ${item.bmi.toFixed(1)}
        </div>
    `;
}

async function loadWorkouts(userId, token) {
    const workoutList = document.getElementById('workoutList');
    if (!workoutList) return;

    try {
        const response = await fetch(`${API_BASE_URL}/workouts/user/${userId}`, {
            headers: buildHeaders(token)
        });
        const workouts = response.ok ? await response.json() : [];

        workoutList.innerHTML = workouts.length
            ? workouts.map(item => renderWorkoutItem(item)).join('')
            : '<p>No workouts yet. Add your first workout below.</p>';
    } catch (error) {
        console.error('loadWorkouts error:', error);
        workoutList.innerHTML = '<p>Unable to load workouts.</p>';
    }
}

function renderWorkoutItem(item) {
    return `
        <div class="item-card">
            <strong>${item.workout_name}</strong><br>
            Duration: ${item.duration} mins<br>
            Calories burned: ${item.calories_burned}
        </div>
    `;
}

async function loadNutrition(userId, token) {
    const nutritionList = document.getElementById('nutritionList');
    if (!nutritionList) return;

    try {
        const response = await fetch(`${API_BASE_URL}/nutrition/user/${userId}`, {
            headers: buildHeaders(token)
        });
        const nutrition = response.ok ? await response.json() : [];

        nutritionList.innerHTML = nutrition.length
            ? nutrition.map(item => renderNutritionItem(item)).join('')
            : '<p>No nutrition entries yet. Add one below.</p>';
    } catch (error) {
        console.error('loadNutrition error:', error);
        nutritionList.innerHTML = '<p>Unable to load nutrition data.</p>';
    }
}

function renderNutritionItem(item) {
    return `
        <div class="item-card">
            <strong>${item.food_name}</strong><br>
            Calories: ${item.calories}<br>
            Protein: ${item.protein} g<br>
            Carbs: ${item.carbs} g
        </div>
    `;
}

function buildHeaders(token) {
    const headers = {
        'Content-Type': 'application/json'
    };
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }
    return headers;
}

async function handleProgressSubmit(e) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');
    const weight = parseFloat(document.getElementById('progressWeight').value);
    const height = parseFloat(document.getElementById('progressHeight').value);

    if (!userId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/progress?user_id=${userId}`, {
            method: 'POST',
            headers: buildHeaders(token),
            body: JSON.stringify({ weight, height })
        });
        if (response.ok) {
            document.getElementById('progressForm').reset();
            await loadProgress(userId, token);
        } else {
            const data = await response.json();
            showMessage('interMessage', data.detail || 'Unable to save progress', 'error');
        }
    } catch (error) {
        console.error('handleProgressSubmit error:', error);
        showMessage('interMessage', 'Error saving progress', 'error');
    }
}

async function handleWorkoutSubmit(e) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');
    const workout_name = document.getElementById('workoutName').value;
    const duration = parseInt(document.getElementById('workoutDuration').value, 10);
    const calories_burned = parseInt(document.getElementById('workoutCalories').value, 10);

    if (!userId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/workouts?user_id=${userId}`, {
            method: 'POST',
            headers: buildHeaders(token),
            body: JSON.stringify({ workout_name, duration, calories_burned })
        });
        if (response.ok) {
            document.getElementById('workoutForm').reset();
            await loadWorkouts(userId, token);
        } else {
            const data = await response.json();
            showMessage('interMessage', data.detail || 'Unable to save workout', 'error');
        }
    } catch (error) {
        console.error('handleWorkoutSubmit error:', error);
        showMessage('interMessage', 'Error saving workout', 'error');
    }
}

async function handleNutritionSubmit(e) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');
    const food_name = document.getElementById('nutritionFood').value;
    const calories = parseInt(document.getElementById('nutritionCalories').value, 10);
    const protein = parseFloat(document.getElementById('nutritionProtein').value);
    const carbs = parseFloat(document.getElementById('nutritionCarbs').value);

    if (!userId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/nutrition?user_id=${userId}`, {
            method: 'POST',
            headers: buildHeaders(token),
            body: JSON.stringify({ food_name, calories, protein, carbs })
        });
        if (response.ok) {
            document.getElementById('nutritionForm').reset();
            await loadNutrition(userId, token);
        } else {
            const data = await response.json();
            showMessage('interMessage', data.detail || 'Unable to save nutrition entry', 'error');
        }
    } catch (error) {
        console.error('handleNutritionSubmit error:', error);
        showMessage('interMessage', 'Error saving nutrition entry', 'error');
    }
}

function renderInterPage(email) {
    const welcomeName = document.getElementById('welcomeName');
    const userEmail = document.getElementById('userEmail');

    if (welcomeName) welcomeName.textContent = email ? email.split('@')[0] : 'User';
    if (userEmail) userEmail.textContent = email || '';

    const progressForm = document.getElementById('progressForm');
    const workoutForm = document.getElementById('workoutForm');
    const nutritionForm = document.getElementById('nutritionForm');

    if (progressForm) progressForm.addEventListener('submit', handleProgressSubmit);
    if (workoutForm) workoutForm.addEventListener('submit', handleWorkoutSubmit);
    if (nutritionForm) nutritionForm.addEventListener('submit', handleNutritionSubmit);
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    localStorage.removeItem('userId');
    window.location.href = 'index.html';
}

window.addEventListener('load', async () => {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    const userId = localStorage.getItem('userId');

    if (interPage) {
        if (!token || !email) {
            window.location.href = 'index.html';
            return;
        }

        renderInterPage(email);
        let resolvedUserId = userId;
        if (!resolvedUserId) {
            resolvedUserId = await fetchUserIdByEmail(email);
            if (resolvedUserId) {
                localStorage.setItem('userId', resolvedUserId);
            }
        }

        if (!resolvedUserId) {
            showMessage('interMessage', 'Unable to determine user. Please login again.', 'error');
            return;
        }

        await loadDashboardData(resolvedUserId, token);
        return;
    }

    if (token && email && loginForm) {
        window.location.href = 'inter.html';
    }
});
