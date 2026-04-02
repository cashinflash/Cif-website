/* ═══════════════════════════════════════
   CASH IN FLASH — MAIN JAVASCRIPT
   ═══════════════════════════════════════ */

(function () {
  'use strict';

  /* ---------- STICKY HEADER SHADOW ---------- */
  var header = document.getElementById('site-header');
  window.addEventListener('scroll', function () {
    header.classList.toggle('scrolled', window.scrollY > 10);
  });

  /* ---------- MOBILE MENU ---------- */
  var toggle = document.getElementById('menu-toggle');
  var mobileMenu = document.getElementById('mobile-menu');
  var overlay = document.getElementById('mobile-overlay');

  function openMenu() {
    toggle.classList.add('active');
    mobileMenu.classList.add('open');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    toggle.classList.remove('active');
    mobileMenu.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  toggle.addEventListener('click', function () {
    mobileMenu.classList.contains('open') ? closeMenu() : openMenu();
  });
  overlay.addEventListener('click', closeMenu);

  /* Mobile sub-menu toggles */
  document.querySelectorAll('.mobile-nav-item.has-sub > a').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      this.parentElement.classList.toggle('open');
    });
  });

  /* ---------- SCROLL ANIMATIONS ---------- */
  var animatedEls = document.querySelectorAll('.animate-on-scroll');
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  animatedEls.forEach(function (el) { observer.observe(el); });

  /* ---------- EDUCATION CAROUSEL ---------- */
  var track = document.getElementById('carousel-track');
  var dotsContainer = document.getElementById('carousel-dots');

  if (track && dotsContainer) {
    var slides = track.querySelectorAll('.carousel-slide');
    var totalOriginal = slides.length / 2; // slides are duplicated in HTML
    var currentPage = 0;

    function getSlidesPerView() {
      if (window.innerWidth <= 768) return 1;
      if (window.innerWidth <= 1024) return 2;
      return 3;
    }

    function getTotalPages() {
      return Math.ceil(totalOriginal / getSlidesPerView());
    }

    function buildDots() {
      dotsContainer.innerHTML = '';
      var pages = getTotalPages();
      for (var i = 0; i < pages; i++) {
        var dot = document.createElement('span');
        dot.className = 'dot' + (i === currentPage ? ' active' : '');
        dot.dataset.page = i;
        dot.addEventListener('click', function () {
          goToPage(parseInt(this.dataset.page));
        });
        dotsContainer.appendChild(dot);
      }
    }

    function goToPage(page) {
      var perView = getSlidesPerView();
      var pages = getTotalPages();
      currentPage = Math.max(0, Math.min(page, pages - 1));
      var slideWidth = track.parentElement.offsetWidth / perView;
      track.style.transform = 'translateX(' + -(currentPage * perView * slideWidth) + 'px)';

      dotsContainer.querySelectorAll('.dot').forEach(function (d, i) {
        d.classList.toggle('active', i === currentPage);
      });
    }

    buildDots();
    window.addEventListener('resize', function () {
      buildDots();
      goToPage(0);
    });

    /* Touch/swipe support */
    var startX = 0;
    var isDragging = false;

    track.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX;
      isDragging = true;
    });
    track.addEventListener('touchend', function (e) {
      if (!isDragging) return;
      isDragging = false;
      var diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) {
        goToPage(currentPage + (diff > 0 ? 1 : -1));
      }
    });
  }

  /* ---------- FAQ ACCORDION (single open) ---------- */
  var faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(function (item) {
    item.addEventListener('toggle', function () {
      if (this.open) {
        faqItems.forEach(function (other) {
          if (other !== item) other.removeAttribute('open');
        });
      }
    });
  });

})();
