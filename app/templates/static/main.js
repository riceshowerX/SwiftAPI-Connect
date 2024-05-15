$(document).ready(function () {
    const maxRetry = 3;
    const retryInterval = 1000; // 重试间隔时间（毫秒）
  
    $("#request-form").submit(async function (event) {
      event.preventDefault();
      const form = $(this);
      const url = encodeURIComponent(form.find("input[name='url']").val());
      const method = form.find("select[name='method']").val();
      const encoding = form.find("select[name='encoding']").val();
      const data = encodeURIComponent(form.find("textarea[name='data']").val());
      const customHeaders = encodeURIComponent(form.find("input[name='custom-headers']").val());
      const cookie = encodeURIComponent(form.find("input[name='cookie']").val());
      const proxy = encodeURIComponent(form.find("input[name='proxy']").val());
  
      let retryCount = 0;
      const retryDelays = [0, 1000, 4000, 9000]; // 指数退避重试延迟
  
      async function doRequest() {
        try {
          const response = await fetch(`/request?url=${url}&method=${method}&encoding=${encoding}&data=${data}&custom_headers=${customHeaders}&cookie=${cookie}&proxy=${proxy}`);
          const responseData = await response.json();
          handleResponse(responseData);
        } catch (error) {
          console.error("Error:", error);
          if (retryCount < maxRetry) {
            retryCount++;
            const delay = retryDelays[retryCount] || retryInterval;
            console.log(`Retrying (${retryCount}/${maxRetry}) in ${delay / 1000} seconds...`);
            setTimeout(doRequest, delay);
          } else {
            alert("发送请求失败，请检查URL并重试。");
          }
        }
      }
  
      doRequest();
    });
  
    function handleResponse(data) {
      const log = $("#log");
      const message = data.message || "请求成功，但未提供消息。";
      const logMessage = data.log || "";
      const filteredLog = logMessage.length > 500 ? logMessage.substr(0, 500) + "..." : logMessage;
      log.text(`${message}\n${filteredLog}`);
      log.removeClass().addClass(data.success ? "success" : "error");
      setTimeout(() => {
        log.removeClass().addClass("log");
      }, 3000);
    }
  });