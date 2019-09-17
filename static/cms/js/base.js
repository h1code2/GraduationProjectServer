/**
 * Created by Administrator on 2016/12/17.
 */

$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if (that.children('a').attr('href') == '#') {
            event.preventDefault();
        }
        if (that.parent().hasClass('unfold')) {
            that.parent().removeClass('unfold');
        } else {
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration', 'none');
    });
});


$(function () {
    var url = window.location.href;
    if (url.indexOf('userInfo') >= 0) {
        var userInfoLi = $('.user-info-manage');
        userInfoLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('openLockLogs') >= 0) {
        var openLockLogsLi = $('.open-lock-manage');
        openLockLogsLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('refreshLock') >= 0) {
        var refreshLockLi = $('.refresh-lock-manage');
        refreshLockLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('userManage') >= 0) {
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('lockManage') >= 0) {
        var lockManageLi = $('.lock-manage');
        lockManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('cmsuser_manage') >= 0) {
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('cmsrole_manage') >= 0) {
        var cmsroleManageLi = $('.cmsrole-manage');
        cmsroleManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('banners') >= 0) {
        var bannerManageLi = $('.banner-manage');
        bannerManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});