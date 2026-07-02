// =============================================
// منصة الإمام مالك - إدارة الكناشة
// =============================================

// حالة التعديل
let editingNoteId = null;
const notesList = document.getElementById('notes-list');
const noteForm = document.getElementById('note-form');
const noteContent = document.getElementById('note-content');
const noteCategory = document.getElementById('note-category');
const saveNoteBtn = document.getElementById('save-note-btn');
const cancelEditBtn = document.getElementById('cancel-edit-btn');
const newNoteBtn = document.getElementById('new-note-btn');

// تصنيفات الفوائد مع الألوان
const categoryLabels = {
    'fiqh': 'فقه',
    'lugha': 'لغة',
    'usool': 'أصول فقه',
    'hadith': 'حديث',
    'seerah': 'سيرة',
    'general': 'فائدة عامة',
};

// تحميل جميع الفوائد
async function loadNotes() {
    try {
        notesList.innerHTML = '<div class="loading"><div class="spinner"></div><p>جاري تحميل الفوائد...</p></div>';
        
        const notes = await apiRequest('/api/notes/');
        
        if (notes.length === 0) {
            notesList.innerHTML = '<p style="text-align: center; color: #6b7280; padding: 40px;">لا توجد فوائد حالياً 🗒️</p>';
            return;
        }
        
        renderNotes(notes);
    } catch (error) {
        notesList.innerHTML = `<p style="text-align: center; color: #dc2626; padding: 40px;">حدث خطأ: ${error.message}</p>`;
    }
}

// عرض الفوائد
function renderNotes(notes) {
    notesList.innerHTML = '';
    
    notes.forEach(note => {
        const card = document.createElement('div');
        card.className = 'note-card';
        
        const catClass = `cat-${note.category}`;
        const catLabel = categoryLabels[note.category] || note.category;
        
        card.innerHTML = `
            <span class="note-category ${catClass}">${catLabel}</span>
            <p class="note-content">${escapeHtml(note.content)}</p>
            <div class="note-actions">
                <span class="note-date">${formatDate(note.updated_at)}</span>
                <button class="btn btn-outline btn-sm edit-btn" data-id="${note.id}">✏️ تعديل</button>
                <button class="btn btn-danger btn-sm delete-btn" data-id="${note.id}">🗑️ حذف</button>
            </div>
        `;
        
        notesList.appendChild(card);
    });
    
    // إضافة أحداث الأزرار
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => editNote(parseInt(btn.dataset.id)));
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => deleteNote(parseInt(btn.dataset.id)));
    });
}

// إظهار نموذج الإضافة
function showAddForm() {
    editingNoteId = null;
    noteForm.style.display = 'block';
    noteContent.value = '';
    noteCategory.value = 'general';
    saveNoteBtn.textContent = '💾 حفظ';
    cancelEditBtn.style.display = 'none';
    newNoteBtn.style.display = 'none';
    noteContent.focus();
    window.scrollTo(0, noteForm.offsetTop - 80);
}

// إخفاء نموذج الإضافة
function hideForm() {
    noteForm.style.display = 'none';
    editingNoteId = null;
    noteContent.value = '';
    noteCategory.value = 'general';
    saveNoteBtn.textContent = '💾 حفظ';
    cancelEditBtn.style.display = 'none';
    newNoteBtn.style.display = 'block';
}

// تعديل فائدة
async function editNote(noteId) {
    try {
        const notes = await apiRequest('/api/notes/');
        const note = notes.find(n => n.id === noteId);
        
        if (!note) {
            showToast('الملاحظة غير موجودة');
            return;
        }
        
        editingNoteId = noteId;
        noteContent.value = note.content;
        noteCategory.value = note.category;
        saveNoteBtn.textContent = '💾 تحديث';
        cancelEditBtn.style.display = 'inline-block';
        newNoteBtn.style.display = 'none';
        noteForm.style.display = 'block';
        noteContent.focus();
        window.scrollTo(0, noteForm.offsetTop - 80);
    } catch (error) {
        showToast('حدث خطأ أثناء جلب الملاحظة');
    }
}

// حفظ فائدة (إضافة أو تحديث)
async function saveNote() {
    const content = noteContent.value.trim();
    const category = noteCategory.value;
    
    if (!content) {
        showToast('الرجاء كتابة الفائدة');
        return;
    }
    
    try {
        if (editingNoteId) {
            await apiRequest(`/api/notes/${editingNoteId}`, {
                method: 'PUT',
                body: JSON.stringify({ content, category }),
            });
            showToast('تم تحديث الفائدة بنجاح ✅');
        } else {
            await apiRequest('/api/notes/', {
                method: 'POST',
                body: JSON.stringify({ content, category }),
            });
            showToast('تم حفظ الفائدة بنجاح ✅');
        }
        
        hideForm();
        await loadNotes();
    } catch (error) {
        showToast(`خطأ: ${error.message}`);
    }
}

// حذف فائدة
async function deleteNote(noteId) {
    if (!confirm('هل أنت متأكد من حذف هذه الفائدة؟')) {
        return;
    }
    
    try {
        await apiRequest(`/api/notes/${noteId}`, {
            method: 'DELETE',
        });
        showToast('تم حذف الفائدة بنجاح 🗑️');
        await loadNotes();
    } catch (error) {
        showToast(`خطأ: ${error.message}`);
    }
}

// أدوات مساعدة
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// أحداث الأزرار
newNoteBtn?.addEventListener('click', showAddForm);
cancelEditBtn?.addEventListener('click', hideForm);
saveNoteBtn?.addEventListener('click', saveNote);

// إخفاء النموذج بدايةً
hideForm();
