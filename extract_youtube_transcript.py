import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import TranscriptsDisabled

i = """
<body class="with-left-side course-menu-expanded modules primary-nav-transitions context-course_125079 responsive_student_grades_page rmit_hc_flag ally-tooltips-enabled ff no-touch vsc-initialized"><div id="EesySupportCenterReact"><link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&amp;display=swap" rel="stylesheet"><div class="EesySupportCenterReactStyles"></div></div><div></div>

<noscript>
  <div role="alert" class="ic-flash-static ic-flash-error">
    <div class="ic-flash__icon" aria-hidden="true">
      <i class="icon-warning"></i>
    </div>
    <h1>You need to have JavaScript enabled in order to access this site.</h1>
  </div>
</noscript>




<div id="flash_message_holder"></div>
<div id="flash_screenreader_holder" role="alert" aria-live="assertive" aria-relevant="additions" class="screenreader-only" aria-atomic="true"></div>

<div id="application" class="ic-app">
  



<header id="mobile-header" class="no-print">
  <button type="button" class="Button Button--icon-action-rev Button--large mobile-header-hamburger">
    <i class="icon-solid icon-hamburger"></i>
    <span id="mobileHeaderInboxUnreadBadge" class="menu-item__badge" style="min-width: 0; top: 12px; height: 12px; right: 6px; display:none;"></span>
    <span class="screenreader-only">Dashboard</span>
  </button>
  <div class="mobile-header-space"></div>
    <a class="mobile-header-title expandable" href="/courses/125079" role="button" aria-controls="mobileContextNavContainer">
      <div>COSC2123</div>
        <div>What happens at Google interviews (a mock interview)</div>
    </a>
    <div class="mobile-header-space"></div>
    <button type="button" class="Button Button--icon-action-rev Button--large mobile-header-arrow" aria-label="Navigation Menu">
      <i class="icon-arrow-open-down" id="mobileHeaderArrowIcon"></i>
    </button>
</header>
<nav id="mobileContextNavContainer" aria-expanded="false"></nav>

<header id="header" class="ic-app-header no-print ">
  <a href="#content" id="skip_navigation_link">Skip To Content</a>
  <div role="region" class="ic-app-header__main-navigation" aria-label="Global Navigation">
    <ul id="menu" class="ic-app-header__menu-list">
        <li class="menu-item ic-app-header__menu-list-item ">
          <a id="global_nav_profile_link" role="button" href="/profile/settings" class="ic-app-header__menu-list-link">
            <div class="menu-item-icon-container">
              <div aria-hidden="true" class="fs-exclude ic-avatar ">
                <img src="https://rmit.instructure.com/images/thumbnails/30966746/5NAS0Wv033i4Ggn65EcqbLpptusnaCtdnkK305o2" alt="Alessandro Mortimer">
              </div>
              <span class="menu-item__badge"></span>
            </div>
            <div class="menu-item__text">
              Account
            </div>
          </a>
        </li>
      <li class="ic-app-header__menu-list-item ">
        <a id="global_nav_dashboard_link" href="https://rmit.instructure.com/" class="ic-app-header__menu-list-link">
          <div class="menu-item-icon-container" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg ic-icon-svg--dashboard" version="1.1" x="0" y="0" viewBox="0 0 280 200" enable-background="new 0 0 280 200" xml:space="preserve"><path d="M273.09,180.75H197.47V164.47h62.62A122.16,122.16,0,1,0,17.85,142a124,124,0,0,0,2,22.51H90.18v16.29H6.89l-1.5-6.22A138.51,138.51,0,0,1,1.57,142C1.57,65.64,63.67,3.53,140,3.53S278.43,65.64,278.43,142a137.67,137.67,0,0,1-3.84,32.57ZM66.49,87.63,50.24,71.38,61.75,59.86,78,76.12Zm147,0L202,76.12l16.25-16.25,11.51,11.51ZM131.85,53.82v-23h16.29v23Zm15.63,142.3a31.71,31.71,0,0,1-28-16.81c-6.4-12.08-15.73-72.29-17.54-84.25a8.15,8.15,0,0,1,13.58-7.2c8.88,8.21,53.48,49.72,59.88,61.81a31.61,31.61,0,0,1-27.9,46.45ZM121.81,116.2c4.17,24.56,9.23,50.21,12,55.49A15.35,15.35,0,1,0,161,157.3C158.18,152,139.79,133.44,121.81,116.2Z"></path></svg>

          </div>
          <div class="menu-item__text">
            Dashboard
          </div>
        </a>
      </li>
        <li class="menu-item ic-app-header__menu-list-item ic-app-header__menu-list-item--active" aria-current="page">
          <a id="global_nav_courses_link" role="button" href="/courses" class="ic-app-header__menu-list-link">
            <div class="menu-item-icon-container" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg ic-icon-svg--courses" version="1.1" x="0" y="0" viewBox="0 0 280 259" enable-background="new 0 0 280 259" xml:space="preserve"><path d="M73.31,198c-11.93,0-22.22,8-24,18.73a26.67,26.67,0,0,0-.3,3.63v.3a22,22,0,0,0,5.44,14.65,22.47,22.47,0,0,0,17.22,8H200V228.19h-134V213.08H200V198Zm21-105.74h90.64V62H94.3ZM79.19,107.34V46.92H200v60.42Zm7.55,30.21V122.45H192.49v15.11ZM71.65,16.71A22.72,22.72,0,0,0,49,39.36V190.88a41.12,41.12,0,0,1,24.32-8h157V16.71ZM33.88,39.36A37.78,37.78,0,0,1,71.65,1.6H245.36V198H215.15v45.32h22.66V258.4H71.65a37.85,37.85,0,0,1-37.76-37.76Z"></path></svg>

            </div>
            <div class="menu-item__text">
              Courses
            </div>
          </a>
        </li>
        <li class="menu-item ic-app-header__menu-list-item ">
          <a id="global_nav_groups_link" role="button" href="/groups" class="ic-app-header__menu-list-link">
            <div class="menu-item-icon-container" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg ic-icon-svg--groups" viewBox="0 0 200 135"><path d="M134.5 129.4c0-1.1 0-19.8-6.2-31.1-4.5-8.5-16.4-12.4-35-19.2-1.7-.6-3.4-1.1-5.1-1.7v-8.5c5.6-5.1 8.5-12.4 8.5-20.3V29.4C96.6 13 83.6 0 67.2 0S37.9 13 37.9 29.4v19.2c0 7.3 3.4 14.7 8.5 20.3v8.5c-1.7.6-3.4 1.1-5.1 1.7-18.6 6.2-30.5 10.7-35 19.2C0 109.6 0 128.8 0 129.4c0 3.4 2.3 5.6 5.6 5.6h123.7c3.5 0 5.7-2.3 5.2-5.6zm-123.2-5.7c.6-5.6 1.7-14.7 3.4-19.8C17 98.8 30 94.3 43.5 89.8c2.8-1.1 5.6-2.3 9-3.4 2.3-.6 4-2.8 4-5.1V66.7c0-1.7-.6-3.4-1.7-4.5-4-3.4-6.2-8.5-6.2-13.6V29.4c0-10.2 7.9-18.1 18.1-18.1s18.1 7.9 18.1 18.1v19.2c0 5.1-2.3 10.2-6.2 13.6-1.1 1.1-1.7 2.8-1.7 4.5v14.7c0 2.3 1.7 4.5 4 5.1 2.8 1.1 6.2 2.3 9 3.4 13.6 5.1 26.6 9.6 28.8 14.1 2.8 5.1 4 13.6 4.5 19.8H11.3zM196 79.1c-2.8-6.2-11.3-9.6-22.6-13.6l-1.7-.6v-3.4c4.5-4 6.8-9.6 6.8-15.8V35c0-12.4-9.6-22-22-22s-22 10.2-22 22v10.7c0 6.2 2.3 11.9 6.8 15.8V65l-1.7.6c-7.3 2.8-13 4.5-16.9 7.3-1.7 1.1-2.3 2.8-2.3 5.1.6 1.7 1.7 3.4 3.4 4.5 7.9 4 12.4 7.3 14.1 10.7 2.3 4.5 4 10.2 5.1 18.1.6 2.3 2.8 4.5 5.6 4.5h45.8c3.4 0 5.6-2.8 5.6-5.1 0-3.9 0-24.3-4-31.6zm-42.9 25.4c-1.1-6.8-2.8-12.4-5.1-16.9-1.7-4-5.1-6.8-9.6-10.2 1.7-1.1 3.4-1.7 5.1-2.3l5.6-2.3c1.7-.6 3.4-2.8 3.4-5.1v-9.6c0-1.7-.6-3.4-2.3-4.5-2.8-1.7-4.5-5.1-4.5-8.5V34.5c0-6.2 4.5-10.7 10.7-10.7s10.7 5.1 10.7 10.7v10.7c0 3.4-1.7 6.2-4.5 8.5-1.1 1.1-2.3 2.8-2.3 4.5v10.2c0 2.3 1.1 4.5 3.4 5.1l5.6 2.3c6.8 2.3 15.3 5.6 16.4 7.9 1.7 2.8 2.8 12.4 2.8 20.9h-35.4z"></path></svg>

            </div>
            <div class="menu-item__text">
              Groups
            </div>
          </a>
        </li>
      <li class="menu-item ic-app-header__menu-list-item ">
        <a id="global_nav_calendar_link" href="/calendar" class="ic-app-header__menu-list-link">
          <div class="menu-item-icon-container" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg ic-icon-svg--calendar" version="1.1" x="0" y="0" viewBox="0 0 280 280" enable-background="new 0 0 280 280" xml:space="preserve"><path d="M197.07,213.38h16.31V197.07H197.07Zm-16.31,16.31V180.76h48.92v48.92Zm-48.92-16.31h16.31V197.07H131.85Zm-16.31,16.31V180.76h48.92v48.92ZM66.62,213.38H82.93V197.07H66.62ZM50.32,229.68V180.76H99.24v48.92Zm146.75-81.53h16.31V131.85H197.07Zm-16.31,16.31V115.54h48.92v48.92Zm-48.92-16.31h16.31V131.85H131.85Zm-16.31,16.31V115.54h48.92v48.92ZM66.62,148.15H82.93V131.85H66.62ZM50.32,164.46V115.54H99.24v48.92ZM34,262.29H246V82.93H34ZM246,66.62V42.16A8.17,8.17,0,0,0,237.84,34H213.38v8.15a8.15,8.15,0,1,1-16.31,0V34H82.93v8.15a8.15,8.15,0,0,1-16.31,0V34H42.16A8.17,8.17,0,0,0,34,42.16V66.62Zm-8.15-48.92a24.49,24.49,0,0,1,24.46,24.46V278.6H17.71V42.16A24.49,24.49,0,0,1,42.16,17.71H66.62V9.55a8.15,8.15,0,0,1,16.31,0v8.15H197.07V9.55a8.15,8.15,0,1,1,16.31,0v8.15Z"></path></svg>

          </div>
          <div class="menu-item__text">
            Calendar
          </div>
        </a>
      </li>
      <li class="menu-item ic-app-header__menu-list-item ">
      <!-- TODO: Add back global search when available -->
        <a id="global_nav_conversations_link" href="/conversations" class="ic-app-header__menu-list-link">
          <div class="menu-item-icon-container">
            <span aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg ic-icon-svg--inbox" version="1.1" x="0" y="0" viewBox="0 0 280 280" enable-background="new 0 0 280 280" xml:space="preserve"><path d="M91.72,120.75h96.56V104.65H91.72Zm0,48.28h80.47V152.94H91.72Zm0-96.56h80.47V56.37H91.72Zm160.94,34.88H228.52V10.78h-177v96.56H27.34A24.17,24.17,0,0,0,3.2,131.48V244.14a24.17,24.17,0,0,0,24.14,24.14H252.66a24.17,24.17,0,0,0,24.14-24.14V131.48A24.17,24.17,0,0,0,252.66,107.34Zm0,16.09a8.06,8.06,0,0,1,8,8v51.77l-32.19,19.31V123.44ZM67.58,203.91v-177H212.42v177ZM27.34,123.44H51.48v79.13L19.29,183.26V131.48A8.06,8.06,0,0,1,27.34,123.44ZM252.66,252.19H27.34a8.06,8.06,0,0,1-8-8V202l30,18H230.75l30-18v42.12A8.06,8.06,0,0,1,252.66,252.19Z"></path></svg>
</span>
            <span class="menu-item__badge"></span>
          </div>
          <div class="menu-item__text">
            Inbox
          </div>
        </a>
      </li>
        <li class="menu-item ic-app-header__menu-list-item">
          <a id="global_nav_history_link" role="button" href="#" class="ic-app-header__menu-list-link">
            <div class="menu-item-icon-container" aria-hidden="true">
              <svg viewBox="0 0 1920 1920" class="ic-icon-svg menu-item__icon svg-icon-history" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <path d="M960 112.941c-467.125 0-847.059 379.934-847.059 847.059 0 467.125 379.934 847.059 847.059 847.059 467.125 0 847.059-379.934 847.059-847.059 0-467.125-379.934-847.059-847.059-847.059M960 1920C430.645 1920 0 1489.355 0 960S430.645 0 960 0s960 430.645 960 960-430.645 960-960 960m417.905-575.955L903.552 988.28V395.34h112.941v536.47l429.177 321.77-67.765 90.465z" stroke="none" stroke-width="1" fill-rule="evenodd"></path>
</svg>
            </div>
            <div class="menu-item__text">
              History
            </div>
          </a>
        </li>
        
    <li id="context_external_tool_38_menu_item" class="globalNavExternalTool menu-item ic-app-header__menu-list-item">
      <a class="ic-app-header__menu-list-link" href="/accounts/1/external_tools/38?launch_type=global_navigation">
          <svg version="1.1" class="ic-icon-svg ic-icon-svg--lti menu-item__icon" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64">
            <path d="M37.5331419,41.3325083 L25.3997411,41.3325083 L25.3997411,52.8756632 C27.5972597,53.6451225 29.1733531,55.7378472 29.1733531,58.198822 C29.1733531,61.3127847 26.6499049,63.8371501 23.5370738,63.8371501 C20.4242427,63.8371501 17.9007945,61.3127847 17.9007945,58.198822 C17.9007945,55.7378472 19.4768879,53.6451225 21.6744065,52.8756632 L21.6744065,41.3325083 L17.5706263,41.3325083 L17.5717453,47.9192726 C17.5717453,50.4825483 15.4945548,52.5604939 12.9322104,52.5604939 L10.9667199,52.5588751 C10.2051449,54.7710384 8.10625368,56.3604121 5.63627929,56.3604121 C2.52344819,56.3604121 2.84217094e-14,53.8360466 2.84217094e-14,50.722084 C2.84217094e-14,47.6081214 2.52344819,45.0837559 5.63627929,45.0837559 C8.08603407,45.0837559 10.1707563,46.6472143 10.9477485,48.8310912 L12.9905507,48.8310912 C13.4625615,48.8310912 13.8452018,48.4483118 13.8452018,47.9761294 L13.8452018,41.3325083 L5.65400042,41.3325083 C4.57511859,41.3325083 3.70051205,40.4575839 3.70051205,39.3783099 L3.70051205,1.95419847 C3.70051205,0.874924458 4.57511859,-1.42108547e-14 5.65400042,-1.42108547e-14 L57.2376164,-1.42108547e-14 C58.3164983,-1.42108547e-14 59.1911048,0.874924458 59.1911048,1.95419847 L59.1911048,39.3783099 C59.1911048,40.4575839 58.3164983,41.3325083 57.2376164,41.3325083 L49.085452,41.3325083 L49.085452,47.9761294 C49.085452,48.4483118 49.4680923,48.8310912 49.9401031,48.8310912 L51.9829054,48.8310912 C52.7598976,46.6472143 54.8446197,45.0837559 57.2943745,45.0837559 C60.4072056,45.0837559 62.9306538,47.6081214 62.9306538,50.722084 C62.9306538,53.8360466 60.4072056,56.3604121 57.2943745,56.3604121 C54.8244001,56.3604121 52.725509,54.7710384 51.9639339,52.5588751 L49.9996524,52.5604938 C47.436099,52.5604939 45.3589085,50.4825483 45.3589085,47.9192726 L45.3600275,41.3325083 L41.2584765,41.3325083 L41.2584765,52.8756632 C43.4559951,53.6451225 45.0320885,55.7378472 45.0320885,58.198822 C45.0320885,61.3127847 42.5086403,63.8371501 39.3958092,63.8371501 C36.2829781,63.8371501 33.7595299,61.3127847 33.7595299,58.198822 C33.7595299,55.7378472 35.3356233,53.6451225 37.5331419,52.8756632 L37.5331419,41.3325083 Z M39.4407163,60.0484002 C40.4618389,60.0484002 41.2896223,59.2203158 41.2896223,58.198822 C41.2896223,57.1773282 40.4618389,56.3492439 39.4407163,56.3492439 C38.4195937,56.3492439 37.5918102,57.1773282 37.5918102,58.198822 C37.5918102,59.2203158 38.4195937,60.0484002 39.4407163,60.0484002 Z M23.5819809,60.0484002 C24.6031035,60.0484002 25.4308869,59.2203158 25.4308869,58.198822 C25.4308869,57.1773282 24.6031035,56.3492439 23.5819809,56.3492439 C22.5608582,56.3492439 21.7330748,57.1773282 21.7330748,58.198822 C21.7330748,59.2203158 22.5608582,60.0484002 23.5819809,60.0484002 Z M57.3392816,52.5716621 C58.3604042,52.5716621 59.1881877,51.7435778 59.1881877,50.722084 C59.1881877,49.7005902 58.3604042,48.8725058 57.3392816,48.8725058 C56.318159,48.8725058 55.4903755,49.7005902 55.4903755,50.722084 C55.4903755,51.7435778 56.318159,52.5716621 57.3392816,52.5716621 Z M5.59137222,52.5716621 C6.61249484,52.5716621 7.44027829,51.7435778 7.44027829,50.722084 C7.44027829,49.7005902 6.61249484,48.8725058 5.59137222,48.8725058 C4.57024959,48.8725058 3.74246615,49.7005902 3.74246615,50.722084 C3.74246615,51.7435778 4.57024959,52.5716621 5.59137222,52.5716621 Z M30.1554353,12.9293586 L35.7525093,16.2831044 C36.070684,16.5163802 36.2591714,16.8906762 36.2591714,17.2892282 C36.2591714,17.6877801 36.070684,18.0620761 35.7525093,18.2953519 L30.1554353,21.6490977 C29.7776345,21.8706324 29.3121961,21.8707698 28.9342686,21.6494581 C28.5563411,21.4281465 28.3232712,21.0189676 28.3227651,20.575899 L28.3227651,14.0025573 C28.3232712,13.5594887 28.5563411,13.1503099 28.9342686,12.9289982 C29.3121961,12.7076865 29.7776345,12.7078239 30.1554353,12.9293586 Z M55.6445081,31.031948 L55.6445081,4.52360758 C55.6445081,3.98397057 55.2072048,3.54650834 54.6677639,3.54650834 L8.22385298,3.54650834 C7.68441206,3.54650834 7.24710879,3.98397057 7.24710879,4.52360758 L7.24710879,31.031948 L55.6445081,31.031948 Z M55.6445081,34.5784563 L7.24710879,34.5784563 L7.24710879,36.8093831 C7.24710879,37.3490201 7.68441206,37.7864824 8.22385298,37.7864824 L54.6677639,37.7864824 C55.2072048,37.7864824 55.6445081,37.3490201 55.6445081,36.8093831 L55.6445081,34.5784563 Z"></path>
          </svg>
        <div class="menu-item__text">
          Studio
        </div>
      </a>
    </li>

      <li class="ic-app-header__menu-list-item">
        <a id="global_nav_help_link" role="button" class="ic-app-header__menu-list-link" data-track-category="help system" data-track-label="help button" href="https://help.instructure.com">
          <div class="menu-item-icon-container" role="presentation">
              <svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg menu-item__icon svg-icon-help" version="1.1" x="0" y="0" viewBox="0 0 200 200" enable-background="new 0 0 200 200" xml:space="preserve" fill="currentColor"><path d="M100,127.88A11.15,11.15,0,1,0,111.16,139,11.16,11.16,0,0,0,100,127.88Zm8.82-88.08a33.19,33.19,0,0,1,23.5,23.5,33.54,33.54,0,0,1-24,41.23,3.4,3.4,0,0,0-2.74,3.15v9.06H94.42v-9.06a14.57,14.57,0,0,1,11.13-14,22.43,22.43,0,0,0,13.66-10.27,22.73,22.73,0,0,0,2.31-17.37A21.92,21.92,0,0,0,106,50.59a22.67,22.67,0,0,0-19.68,3.88,22.18,22.18,0,0,0-8.65,17.64H66.54a33.25,33.25,0,0,1,13-26.47A33.72,33.72,0,0,1,108.82,39.8ZM100,5.2A94.8,94.8,0,1,0,194.8,100,94.91,94.91,0,0,0,100,5.2m0,178.45A83.65,83.65,0,1,1,183.65,100,83.73,83.73,0,0,1,100,183.65" transform="translate(-5.2 -5.2)"></path></svg>

            <span class="menu-item__badge"></span>
          </div>
          <div class="menu-item__text">
            Help
          </div>
</a>      </li>
    </ul>
  </div>
  <div class="ic-app-header__secondary-navigation">
    <ul class="ic-app-header__menu-list">
      <li class="menu-item ic-app-header__menu-list-item">
        <a id="primaryNavToggle" role="button" href="#" class="ic-app-header__menu-list-link ic-app-header__menu-list-link--nav-toggle" aria-label="Expand global navigation
                " title="Expand global navigation
                ">
          <div class="menu-item-icon-container" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" class="ic-icon-svg ic-icon-svg--navtoggle" version="1.1" x="0" y="0" width="40" height="32" viewBox="0 0 40 32" xml:space="preserve">
  <path d="M39.5,30.28V2.48H37.18v27.8Zm-4.93-13.9L22.17,4,20.53,5.61l9.61,9.61H.5v2.31H30.14l-9.61,9.61,1.64,1.64Z"></path>
</svg>

          </div>
        </a>
      </li>
    </ul>
  </div>
  <div id="global_nav_tray_container"></div>
  <div id="global_nav_tour"></div>
</header>


  <div id="instructure_ajax_error_box">
    <div style="text-align: right; background-color: #fff;"><a href="#" class="close_instructure_ajax_error_box_link">Close</a></div>
    <iframe id="instructure_ajax_error_result" src="about:blank" style="border: 0;" title="Error"></iframe>
  </div>

  <div id="wrapper" class="ic-Layout-wrapper">
        <div class="ic-app-nav-toggle-and-crumbs no-print">
            <button type="button" id="courseMenuToggle" class="Button Button--link ic-app-course-nav-toggle" aria-live="polite" aria-label="Hide Courses Navigation Menu">
              <i class="icon-hamburger" aria-hidden="true"></i>
            </button>

          <div class="ic-app-crumbs">
              <nav id="breadcrumbs" role="navigation" aria-label="breadcrumbs"><ul><li class="home"><a href="/"><span class="ellipsible ellipsis" style="max-width: 100px;"><i class="icon-home" title="My dashboard">
  <span class="screenreader-only">My dashboard</span>
</i>
</span></a></li><li><a href="/courses/125079"><span class="ellipsible ellipsis" style="max-width: 100px;">COSC2123</span></a></li><li><a href="/courses/125079/modules"><span class="ellipsible ellipsis" style="max-width: 100px;">Modules</span></a></li><li><a href="/courses/125079/modules/1155943"><span class="ellipsible ellipsis" style="max-width: 100px;">Week 1: Introductions &amp; Problem Types</span></a></li><li><span class="ellipsible ellipsis" style="max-width: 100px;">What happens at Google interviews (a mock interview)</span></li></ul></nav>
          </div>


          <div class="right-of-crumbs">
          </div>

        </div>
    <div id="main" class="ic-Layout-columns">
        <div class="ic-Layout-watermark"></div>
        <div id="left-side" class="ic-app-course-menu ic-sticky-on list-view" style="display: block">
          <div id="sticky-container" class="ic-sticky-frame has-scrollbar">
              <span id="section-tabs-header-subtitle" class="ellipsis">UGRD Semester 1 2024 (2410)</span>
            <nav role="navigation" aria-label="Courses Navigation Menu"><ul id="section-tabs"><li class="section"><a href="/courses/125079" class="home" tabindex="0">Home</a></li><li class="section"><a href="/courses/125079/announcements" class="announcements" tabindex="0">Announcements</a></li><li class="section"><a href="/courses/125079/assignments/syllabus" class="syllabus" tabindex="0">Syllabus</a></li><li class="section"><a href="/courses/125079/modules" aria-current="page" class="modules active" tabindex="0">Modules</a></li><li class="section"><a href="/courses/125079/assignments" class="assignments" tabindex="0">Assignments</a></li><li class="section"><a href="/courses/125079/discussion_topics" class="discussions" tabindex="0">Discussions</a></li><li class="section"><a href="/courses/125079/grades" class="grades" tabindex="0">Grades</a></li><li class="section"><a href="/courses/125079/users" class="people" tabindex="0">People</a></li><li class="section"><a href="/courses/125079/wiki" class="pages" tabindex="0">Pages</a></li><li class="section"><a href="/courses/125079/quizzes" class="quizzes" tabindex="0">Quizzes</a></li><li class="section"><a href="/courses/125079/external_tools/546" class="context_external_tool_546" tabindex="0">Collaborate Ultra</a></li><li class="section"><a href="/courses/125079/external_tools/103891?display=borderless" class="context_external_tool_103891" target="_blank" tabindex="0">Study help 24/7 - Studiosity</a></li><li class="section"><a href="/courses/125079/external_tools/160783" class="context_external_tool_160783" tabindex="0">Library and Study Support</a></li></ul></nav>
          </div>
        </div>
      <div id="not_right_side" class="ic-app-main-content">
        <div id="content-wrapper" class="ic-Layout-contentWrapper">
          
          <div id="content" class="ic-Layout-contentMain" role="main">
            
  <h1 class="screenreader-only">What happens at Google interviews (a mock interview)</h1>
    <ul style="margin-top:0" class="ui-listview ui-listview-no-rounded-bottom">
      <li class="active">
        <span style="font-size:18px; text-align: center; padding: .2em" class="ui-listview-text">
          <a href="https://www.youtube.com/embed/XKu_SEDAykw" class="external" target="_blank" rel="noreferrer noopener"><span>What happens at Google interviews (a mock interview)</span><span class="external_link_icon" style="margin-inline-start: 5px; display: inline-block; text-indent: initial; " role="presentation"><svg viewBox="0 0 1920 1920" xmlns="http://www.w3.org/2000/svg" style="width:1em; height:1em; vertical-align:middle; fill:currentColor">
    <path d="M1226.667 267c88.213 0 160 71.787 160 160v426.667H1280v-160H106.667v800C106.667 1523 130.56 1547 160 1547h1066.667c29.44 0 53.333-24 53.333-53.333v-213.334h106.667v213.334c0 88.213-71.787 160-160 160H160c-88.213 0-160-71.787-160-160V427c0-88.213 71.787-160 160-160Zm357.706 442.293 320 320c20.8 20.8 20.8 54.614 0 75.414l-320 320-75.413-75.414 228.907-228.906H906.613V1013.72h831.254L1508.96 784.707l75.413-75.414Zm-357.706-335.626H160c-29.44 0-53.333 24-53.333 53.333v160H1280V427c0-29.333-23.893-53.333-53.333-53.333Z" fill-rule="evenodd"></path>
</svg>
<span class="screenreader-only">Links to an external site.</span></span></a>
        </span>
      </li>
      <li>
        <span style="padding:0" class="ui-listview-text">
          <iframe src="https://www.youtube.com/embed/XKu_SEDAykw" id="file_content" title="What happens at Google interviews (a mock interview)" style="width: 100%; height: 400px; float: left;"></iframe>
          <div class="clear"></div>
        </span>
      </li>
    </ul>


  <div id="sequence_footer" data-course-id="125079" data-asset-id="5924248" data-asset-type="ModuleItem"><div class="module-sequence-padding"></div>
<div class="module-sequence-footer" role="navigation" aria-label="Module Navigation">
  <div class="module-sequence-footer-content">
    
      <span class="module-sequence-footer-button--previous" data-tooltip="right" data-html-tooltip-title="<i class='icon-quiz'></i> Week 1 Quiz">
          <a href="https://rmit.instructure.com/courses/125079/modules/items/5924246" class="Button" aria-describedby="msf0-previous-desc" aria-label="Previous Module Item">
            <i class="icon-mini-arrow-left"></i>Previous
            <span id="msf0-previous-desc" class="hidden" hidden="">Previous: Week 1 Quiz</span>
          </a>
      </span>
    

    
      <span class="module-sequence-footer-button--next" data-tooltip="left" data-html-tooltip-title="<i class='icon-link'></i> Visualisation tool for data structures&amp;#x2F;abstract data types">
        <a href="https://rmit.instructure.com/courses/125079/modules/items/5924249" class="Button" aria-describedby="msf0-next-desc" aria-label="Next Module Item">
          Next<i class="icon-mini-arrow-right"></i>
          <span id="msf0-next-desc" class="hidden" hidden="">Next: Visualisation tool for data structures/abstract data types</span>
        </a>
      </span>
    
  </div>
</div>
</div>



          </div>
        </div>
        <div id="right-side-wrapper" class="ic-app-main-content__secondary">
          <aside id="right-side" role="complementary">
            
          </aside>
        </div>
      </div>
    </div>
  </div>



    <div style="display:none;"><!-- Everything inside of this should always stay hidden -->
        <div id="page_view_id">821dc69c-7f3c-49e9-93cd-4b91ebcd797e</div>
    </div>
  <div id="aria_alerts" class="hide-text affix" role="alert" aria-live="assertive"></div>
  <div id="StudentTray__Container"></div>
  <div id="react-router-portals"></div>
  

  <iframe src="https://sso.canvaslms.com/post_message_forwarding?rev=59677caad5-09bb3c9388a5ba3a&amp;token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJwYXJlbnRfZG9tYWluIjoicm1pdC5pbnN0cnVjdHVyZS5jb20ifQ.QWdtoxDkztLUu2ZvAMOrZ-1_e8VC40sUCF1Y2ZkGeojbYILHl4ltILLpC6rmlufM_lYiL7PYeHy0pqrsx120Ow" name="post_message_forwarding" title="post_message_forwarding" id="post_message_forwarding" sandbox="allow-scripts allow-same-origin" style="display:none;"></iframe>



<script>
//<![CDATA[
(window.bundles || (window.bundles = [])).push('inst_fs_service_worker');
//]]>
</script>
  <script src="https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_95950000000000001/attachments/36961555/1.rmit.production.js" defer="defer"></script>
  <script src="https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_95950000000000001/attachments/30557202/698.rmit.production.js" defer="defer"></script>

</div> <!-- #application -->


<div role="log" aria-live="assertive" aria-relevant="additions" class="ally-helper-hidden-accessible"></div><div id="nav-tray-portal" style="position: relative; z-index: 99;"></div><div id="impact-sr-alert" class="impact-sr-only" aria-live="polite"></div><iframe id="walkme-native-functions" style="display: none; position: absolute; visibility: hidden; z-index: -2147483647;" class="walkme-to-remove"></iframe><iframe id="walkme-proxy-iframe" class="walkme-to-remove" style="display: none; visibility: hidden;" src="about:blank"></iframe><div id="walkme-player" class="walkme-player walkme-colorado walkme-theme-white-blue walkme-direction-ltr walkme-notie walkme-position-major-right walkme-position-minor-bottom  walkme-dynamic-size walkme-to-destroy walkme-override walkme-css-reset walkme-language-default" style="" role="button" aria-label="Need Help" draggable="true"><div class="walkme-in-wrapper walkme-override walkme-css-reset" style="height: 153px;"><div class="walkme-question-mark walkme-override walkme-css-reset"></div><div class="walkme-title walkme-override walkme-css-reset" style="width: 96px; right: -28px; bottom: 44.5px;">Need Help<span class="grippy"></span></div></div></div></body>
"""
# i = """
# https://www.youtube.com/watch?v=DFYRQ_zQ-gk&feature=featured
# https://www.youtube.com/watch?v=DFYRQ_zQ-gk
# http://www.youtube.com/watch?v=DFYRQ_zQ-gk
# //www.youtube.com/watch?v=DFYRQ_zQ-gk
# www.youtube.com/watch?v=DFYRQ_zQ-gk
# https://youtube.com/watch?v=DFYRQ_zQ-gk
# http://youtube.com/watch?v=DFYRQ_zQ-gk
# //youtube.com/watch?v=DFYRQ_zQ-gk
# youtube.com/watch?v=DFYRQ_zQ-gk

# https://m.youtube.com/watch?v=DFYRQ_zQ-gk
# http://m.youtube.com/watch?v=DFYRQ_zQ-gk
# //m.youtube.com/watch?v=DFYRQ_zQ-gk
# m.youtube.com/watch?v=DFYRQ_zQ-gk

# https://www.youtube.com/v/DFYRQ_zQ-gk?fs=1&hl=en_US
# http://www.youtube.com/v/DFYRQ_zQ-gk?fs=1&hl=en_US
# //www.youtube.com/v/DFYRQ_zQ-gk?fs=1&hl=en_US
# www.youtube.com/v/DFYRQ_zQ-gk?fs=1&hl=en_US
# youtube.com/v/DFYRQ_zQ-gk?fs=1&hl=en_US

# https://www.youtube.com/embed/DFYRQ_zQ-gk?autoplay=1
# https://www.youtube.com/embed/DFYRQ_zQ-gk
# http://www.youtube.com/embed/DFYRQ_zQ-gk
# //www.youtube.com/embed/DFYRQ_zQ-gk
# www.youtube.com/embed/DFYRQ_zQ-gk
# https://youtube.com/embed/DFYRQ_zQ-gk
# http://youtube.com/embed/DFYRQ_zQ-gk
# //youtube.com/embed/DFYRQ_zQ-gk
# youtube.com/embed/DFYRQ_zQ-gk

# https://www.youtube-nocookie.com/embed/DFYRQ_zQ-gk?autoplay=1
# https://www.youtube-nocookie.com/embed/DFYRQ_zQ-gk
# http://www.youtube-nocookie.com/embed/DFYRQ_zQ-gk
# //www.youtube-nocookie.com/embed/DFYRQ_zQ-gk
# www.youtube-nocookie.com/embed/DFYRQ_zQ-gk
# https://youtube-nocookie.com/embed/DFYRQ_zQ-gk
# http://youtube-nocookie.com/embed/DFYRQ_zQ-gk
# //youtube-nocookie.com/embed/DFYRQ_zQ-gk
# youtube-nocookie.com/embed/DFYRQ_zQ-gk

# https://youtu.be/DFYRQ_zQ-gk?t=120
# https://youtu.be/DFYRQ_zQ-gk
# http://youtu.be/DFYRQ_zQ-gk
# //youtu.be/DFYRQ_zQ-gk
# youtu.be/DFYRQ_zQ-gk

# https://www.youtube.com/HamdiKickProduction?v=DFYRQ_zQ-gk
# """

youtube_re = r"((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?"


def extract_youtube_transcript(input_string):
    transcript_map = {}
    video_ids = list(set([str(v[-2]) for v in re.findall(youtube_re, input_string) if str(v[-2]) != ""]))
    
    for video_id in video_ids:
        print(video_id)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_map[video_id] = " ".join([d['text'] for d in transcript])
        except TranscriptsDisabled:
            print(f"No transcript for video id: {video_id}")
            continue
        print(transcript)
    
    return transcript_map

o = extract_youtube_transcript(i)
for k in o:
    print(f"{k}\n{o[k]}")