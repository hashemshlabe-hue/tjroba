// =============================================
// منصة الإمام مالك - لوحة تحكم المشرف
// =============================================

const adminChannelsList = document.getElementById('admin-channels-list');
const adminForm = document.getElementById('admin-form');
const channelNameInput = document.getElementById('channel-name');
const channelLinkInput = document.getElementById('channel-link');
const channelTypeInput = document.getElementById('channel-type');
const channelDescInput = document.getElementById('channel-desc');
const saveChannelBtn = document.getElementById('save-channel-btn');
const cancelChannelBtn = document.getElementById('cancel-channel-btn');
const addChannelBtn = document.getElementById('add-channel-btn');

let editingChannelId = null;

// تحميل جميع القنوات للوحة التحكم
async function loadAdminChannels() {
    try {
        adminChannelsList.innerHTML = '<p style="text-align: center; padding: 20px;">جاري التحميل...</p>';
        
        const channels = await apiRequest('/api/admin/channels');
        
        if (channels.length === 0) {
            adminChannelsList.innerHTML = '<p style="text-align: center; color: #6b7280; padding: 40px;">لا توجد قنوات بعد</p>';
            return;
        }
        
        renderAdminTable(channels);
    } catch (error) {
        if (error.message.includes('403') || error.message.includes('غير مصرح')) {
            adminChannelsList.innerHTML = '<p style="text-align: center; color: #dc2626; padding: 40px;">⛔ غير مصرح لك بالوصول</p>';
        } else {
            adminChannelsList.innerHTML = `<p style="text-align: center; color: #dc2626; padding: 40px;">خطأ: ${error.message}</p>`;
        }
    }
}

// عرض الجدول
function renderAdminTable(channels) {
    const typeLabels = {
        'college': 'قنوات الكلية',
        'dawah': 'دعوية وقرآنية',
        'group': 'مجموعات',
    };
    
    let html = '<table class="admin-table"><thead><tr><th>الاسم</th><th>النوع</th><th>الرابط</th><th>الحالة</th><th>إجراءات</th></tr></thead><tbody>';
    
    channels.forEach(ch => {
        const typeLabel = typeLabels[ch.type] || ch.type;
        const statusBadge = ch.is_active 
            ? '<span style="color: #166534;">✅ نشط</span>' 
            : '<span style="color: #dc2626;">❌ معطل</span>';
        
        html += `
            <tr>
                <td>${escapeHtml(ch.name)}</td>
                <td>${typeLabel}</td>
                <td><a href="${escapeHtml(ch.link)}" target="_blank" style="color: #166534;">🔗 فتح</a></td>
                <td>${statusBadge}</td>
                <td>
                    <button class="btn btn-outline btn-sm edit-channel-btn" data-id="${ch.id}">✏️</button>
                    <button class="btn btn-danger btn-sm delete-channel-btn" data-id="${ch.id}">🗑️</button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    adminChannelsList.innerHTML = html;
    
    // أحداث الأزرار
    document.querySelectorAll('.edit-channel-btn').forEach(btn => {
        btn.addEventListener('click', () => editChannel(parseInt(btn.dataset.id)));
    });
    
    document.querySelectorAll('.delete-channel-btn').forEach(btn => {
        btn.addEventListener('click', () => deleteChannel(parseInt(btn.dataset.id)));
    });
}

// إظهار نموذج الإضافة
function showAddChannelForm() {
    editingChannelId = null;
    adminForm.style.display = 'block';
    channelNameInput.value = '';
    channelLinkInput.value = '';
    channelTypeInput.value = 'college';
    channelDescInput.value = '';
    saveChannelBtn.textContent = '💾 إضافة';
    cancelChannelBtn.style.display = 'none';
    addChannelBtn.style.display = 'none';
}

// إخفاء النموذج
function hideChannelForm() {
    adminForm.style.display = 'none';
    editingChannelId = null;
    channelNameInput.value = '';
    channelLinkInput.value = '';
    channelTypeInput.value = 'college';
    channelDescInput.value = '';
    cancelChannelBtn.style.display = 'none';
    addChannelBtn.style.display = 'block';
}

// تعديل قناة
async function editChannel(channelId) {
    try {
        const channels = await apiRequest('/api/admin/channels');
        const channel = channels.find(c => c.id === channelId);
        
        if (!channel) {
            showToast('القناة غير موجودة');
            return;
        }
        
        editingChannelId = channelId;
        channelNameInput.value = channel.name;
        channelLinkInput.value = channel.link;
        channelTypeInput.value = channel.type;
        channelDescInput.value = channel.description || '';
        saveChannelBtn.textContent = '💾 تحديث';
        cancelChannelBtn.style.display = 'inline-block';
        addChannelBtn.style.display = 'none';
        adminForm.style.display = 'block';
    } catch (error) {
        showToast('حدث خطأ أثناء جلب بيانات القناة');
    }
}

// حفظ قناة
async function saveChannel() {
    const name = channelNameInput.value.trim();
    const link = channelLinkInput.value.trim();
    const type = channelTypeInput.value;
    const description = channelDescInput.value.trim();
    
    if (!name || !link) {
        showToast('الرجاء إدخال الاسم والرابط');
        return;
    }
    
    const body = { name, link, type, description: description || null };
    
    try {
        if (editingChannelId) {
            await apiRequest(`/api/admin/channels/${editingChannelId}`, {
                method: 'PUT',
                body: JSON.stringify(body),
            });
            showToast('تم تحديث القناة ✅');
        } else {
            await apiRequest('/api/admin/channels', {
                method: 'POST',
                body: JSON.stringify(body),
            });
            showToast('تم إضافة القناة ✅');
        }
        
        hideChannelForm();
        await loadAdminChannels();
    } catch (error) {
        showToast(`خطأ: ${error.message}`);
    }
}

// حذف قناة
async function deleteChannel(channelId) {
    if (!confirm('هل أنت متأكد من حذف هذه القناة؟')) {
        return;
    }
    
    try {
        await apiRequest(`/api/admin/channels/${channelId}`, {
            method: 'DELETE',
        });
        showToast('تم حذف القناة 🗑️');
        await loadAdminChannels();
    } catch (error) {
        showToast(`خطأ: ${error.message}`);
    }
}

// الأحداث
addChannelBtn?.addEventListener('click', showAddChannelForm);
cancelChannelBtn?.addEventListener('click', hideChannelForm);
saveChannelBtn?.addEventListener('click', saveChannel);

// إخفاء النموذج بدايةً
hideChannelForm();
