(function($) {
    ('use strict');

    /*  ======================================
        Scroll To Menu fixed On Top
    ====================================== */

    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 84) {
            $('.site-header').addClass('fixed-nav');
        } else {
            $('.site-header').removeClass('fixed-nav');
        }
    });

    /*==============================================
        Mobil Nav
    ==============================================*/

    const menuIcon = document.querySelector('.mobile-nav-icon');
    const navbar = document.querySelector('.main-menu');
    const navbarIcon = document.querySelector('.nav-icon .fa-bars');

    menuIcon.addEventListener('click', () => {
        navbar.classList.toggle('show');
        navbarIcon.classList.toggle('fa-xmark');
    });

    /*==============================================
        Banner Slider
    ==============================================*/

    const banner_slide_thumb = new Swiper('.banner-thumb', {
        loop: true,
        slidesPerView: 3,
        freeMode: true,
        watchSlidesProgress: true,
    });

    const banner_slide = new Swiper('.banner-slide', {
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        thumbs: {
            swiper: banner_slide_thumb,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    /*  ======================================
        Counter
    ====================================== */

    let funFactCounter = $('.counter');

    funFactCounter.counterUp({
        delay: 10,
        time: 1000,
    });

    /*  ======================================
        Skill Bar
    ====================================== */

    function animateSkillBar() {
        $('.single-skill-circle').percentcircle({
            fillColor: '#fec731',
            percentWeight: 'normal',
        });
    }

    if ($('.single-skill').length > 0) {
        let waypoint = new Waypoint({
            element: document.getElementsByClassName('single-skill'),
            handler: function(direction) {
                animateSkillBar();
                this.destroy();
            },
            offset: '100%',
        });
    }

    /*  ======================================
        Video Popup
    ====================================== */

    let videoPopup = $('.video-btn a');

    videoPopup.YouTubePopUp({
        autoplay: 0,
    });

    /*  ======================================
        Tesimonial Caro
    ====================================== */

    const tesimonial_caro = new Swiper('.tesimonial-caro', {
        loop: true,
        spaceBetween: 30,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        grabCursor: true,
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            768: {
                slidesPerView: 2,
            },
        },
    });

    /*  ======================================
        Partners Caro
    ====================================== */

    const partners_caro = new Swiper('.partners-carousel', {
        loop: true,
        spaceBetween: 30,
        autoplay: {
            delay: 6000,
            disableOnInteraction: false,
        },
        grabCursor: true,
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            575: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 3,
            },
            992: {
                slidesPerView: 4,
            },
        },
    });

    $(window).on('load', function() {
        /*  ======================================
        Portfolio
        ====================================== */

        $('.portfolio-menu button').on('click', function() {
            $('.portfolio-menu button').removeClass('active-port');
            $(this).addClass('active-port');
        });

        let $container = $('.portfolio-container');
        $container.isotope({
            itemSelector: '.portfolio-container .single-portfolios',
            percentPosition: true,
            masonry: {
                columnWidth: 1,
            },
        });

        $('#filters').on('click', 'button', function() {
            let filterValue = $(this).attr('data-filter');
            $container.isotope({
                filter: filterValue
            });
            return false;
        });
    });
})(jQuery);