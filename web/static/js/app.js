// =============================================
// منصة الإمام مالك التعليمية - JavaScript الرئيسي
// =============================================

// عناصر DOM الرئيسية
const pages = {
    home: document.getElementById('home-page'),
    college: document.getElementById('college-page'),
    dawah: document.getElementById('dawah-page'),
    groups: document.getElementById('groups-page'),
    notes: document.getElementById('notes-page'),
    admin: document.getElementById('admin-page'),
};

// التحقق من بيئة تيليجرام
const tg = window.Telegram?.WebApp;
let initData = '';

if (tg) {
    tg.ready();
    initData = tg.initData || '';
    tg.expand();
} else {
    // للتطوير المحلي بدون تيليجرام
    console.warn('Telegram WebApp غير متوفر، تشغيل في وضع التطوير');
    initData = '';
}

// معرف المستخدم (يُستخرج من initData)
let currentUserId = null;

// دالة استخراج user_id من initData
function getUserIdFromInitData(data) {
    if (!data) return null;
    try {
        const params = new URLSearchParams(data);
        const user = params.get('user');
        if (user) {
            const userObj = JSON.parse(decodeURIComponent(user));
            return userObj.id;
        }
    } catch (e) {
        console.error('خطأ في استخراج user_id:', e);
    }
    return null;
}

currentUserId = getUserIdFromInitData(initData);

// رؤوس الطلبات
function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'X-Init-Data': initData,
    };
}

// =============================================
// التنقل بين الصفحات
// =============================================

function showPage(pageId) {
    // إخفاء جميع الصفحات
    Object.values(pages).forEach(page => {
        if (page) page.classList.remove('active');
    });
    
    // إظهار الصفحة المطلوبة
    const target = document.getElementById(pageId);
    if (target) {
        target.classList.add('active');
        window.scrollTo(0, 0);
    }
}

function goHome() {
    showPage('home-page');
}

// =============================================
// نظام الإشعارات
// =============================================

function showToast(message, duration = 3000) {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// =============================================
// طلبات API العامة
// =============================================

async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: getHeaders(),
            ...options,
        });
        
        if (response.status === 204) return null;
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'حدث خطأ غير متوقع');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// =============================================
// أحداث التنقل
// =============================================

document.addEventListener('DOMContentLoaded', () => {
    // أزرار الرجوع
    document.querySelectorAll('.back-btn').forEach(btn => {
        btn.addEventListener('click', goHome);
    });
    
    // بطاقات الصفحة الرئيسية
    document.getElementById('card-college')?.addEventListener('click', () => {
        showPage('college-page');
        loadChannels('college');
    });
    
    document.getElementById('card-dawah')?.addEventListener('click', () => {
        showPage('dawah-page');
        loadChannels('dawah');
    });
    
    document.getElementById('card-groups')?.addEventListener('click', () => {
        showPage('groups-page');
        loadChannels('groups');
    });
    
    document.getElementById('card-notes')?.addEventListener('click', () => {
        showPage('notes-page');
        loadNotes();
    });
    
    document.getElementById('card-admin')?.addEventListener('click', () => {
        showPage('admin-page');
        loadAdminChannels();
    });
});
