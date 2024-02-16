const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/manager/tickets/'
);

socket.onopen = () => {
    console.log('WebSocket connection established.');
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const statusData = data.data;
    console.log(statusData)

    const isCheckinElement = document.getElementById('is_checkin_status_' + statusData.ticket_id);
    const isOnboardingElement = document.getElementById('is_onboarding_status_' + statusData.ticket_id);

    const statusTrue = '<span class="bg-green-500 text-white text-xs font-medium me-2 px-3 py-1 rounded dark:bg-gray-700 dark:text-green-400">True</span>';
    const statusFalse = '<span class="bg-red-500 text-white text-xs font-medium me-2 px-3 py-1 rounded dark:bg-gray-700 dark:text-red-400">False</span>';

    if (statusData.is_checkin) {
        isCheckinElement.innerHTML = statusTrue;
    } else {
        isCheckinElement.innerHTML = statusFalse;
    }

    if (statusData.is_onboarding) {
        isOnboardingElement.innerHTML = statusTrue;
    } else {
        isOnboardingElement.innerHTML = statusFalse;
    }
};

socket.onclose = () => {
    console.log('WebSocket connection closed.');
};