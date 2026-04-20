// فتح/إغلاق القائمة
function toggleMenu() {
  const menu = document.getElementById('menuLinks');
  menu.classList.toggle('show');
}

// إغلاق القائمة إذا ضغط المستخدم خارجها
document.addEventListener('click', function(event) {
  const menu = document.getElementById('menuLinks');
  const toggleBtn = document.querySelector('.menu-toggle');

  if (menu.classList.contains('show') && !menu.contains(event.target) && !toggleBtn.contains(event.target)) {
    menu.classList.remove('show');
  }
});
