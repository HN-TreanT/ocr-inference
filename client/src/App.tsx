import { Upload, Row, Col, Button, message, Image, Input } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import "./App.css";
import { useState } from "react";
import type { UploadFile, UploadProps } from "antd/es/upload/interface";
import axios from "axios";

function App() {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [imageUrl, setImageUrl] = useState<any>();
  const [extractedText, setExtractedText] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const beforeUpload = (file: File) => {
    const isImage = file.type.startsWith("image/");
    if (!isImage) {
      message.error("Bạn chỉ có thể upload file ảnh!");
      return false;
    }

    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error("Ảnh phải nhỏ hơn 2MB!");
      return false;
    }

    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setImageUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    return false;
  };

  const handleChange: UploadProps["onChange"] = ({
    fileList: newFileList,
    file,
  }) => {
    if (file.status === "removed") {
      setImageUrl(undefined);
      setExtractedText("");
      setSelectedFile(null);
    }
    const latestFile = newFileList.slice(-1);
    setFileList(latestFile);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      message.error("Vui lòng chọn ảnh trước khi upload!");
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8080/ocr", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // Giả sử response.data là một mảng text
      // Chuyển đổi mảng thành chuỗi với mỗi phần tử một dòng
      const formattedText = response.data.join("\n");
      setExtractedText(formattedText);
      message.success("Chuyển file thành công !");
    } catch (error) {
      console.error("Upload error:", error);
      message.error("Chuyển file thất bại!");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="App"
      data-theme="dark"
      style={{
        backgroundColor: "#1a1a1a",
        minHeight: "100vh",
        padding: "20px",
      }}
    >
      <div
        style={{
          width: "80%",
          margin: "0 auto",
          padding: "30px",
          backgroundColor: "#141414",
          borderRadius: "12px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        }}
      >
        <Row gutter={[24, 24]}>
          <Col
            span={11}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "20px",
              padding: "20px",
              backgroundColor: "#262626",
              borderRadius: "8px",
              minHeight: "500px",
            }}
          >
            <div
              style={{
                textAlign: "center",
                color: "#fff",
                marginBottom: "10px",
              }}
            >
              <h3>Ảnh Gốc</h3>
            </div>
            <Upload
              listType="picture-card"
              fileList={fileList}
              beforeUpload={beforeUpload}
              onChange={handleChange}
              maxCount={1}
              action="/dummy"
              showUploadList={{
                showPreviewIcon: true,
                showRemoveIcon: true,
              }}
            >
              {fileList.length === 0 && (
                <div style={{ color: "white" }}>
                  <UploadOutlined />
                  <div style={{ marginTop: 8, marginBottom: 8 }}>
                    Upload Ảnh
                  </div>
                </div>
              )}
            </Upload>
            {imageUrl && (
              <div
                style={{
                  width: "80%",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  backgroundColor: "#1f1f1f",
                  padding: "20px",
                  borderRadius: "8px",
                }}
              >
                <Image
                  src={imageUrl}
                  preview={false}
                  style={{
                    width: "90%",
                    height: "auto",
                    objectFit: "contain",
                    borderRadius: "4px",
                  }}
                />
              </div>
            )}
          </Col>
          <Col
            span={2}
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              padding: "20px",
            }}
          >
            <Button
              type="primary"
              size="large"
              onClick={handleUpload}
              loading={isLoading}
              disabled={!selectedFile}
              style={{
                backgroundColor: "#1890ff",
                borderColor: "#1890ff",
                boxShadow: "0 2px 4px rgba(24, 144, 255, 0.2)",
              }}
            >
              Chuyển
            </Button>
          </Col>
          <Col
            span={11}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              padding: "20px",
              backgroundColor: "#262626",
              borderRadius: "8px",
              minHeight: "500px",
            }}
          >
            <div
              style={{
                textAlign: "center",
                color: "#fff",
                marginBottom: "10px",
              }}
            >
              <h3>Text Trích Xuất</h3>
            </div>
            <div
              style={{
                width: "100%",
                height: "100%",
                backgroundColor: "#1f1f1f",
                padding: "20px",
                borderRadius: "8px",
              }}
            >
              <Input.TextArea
                value={extractedText}
                onChange={(e) => setExtractedText(e.target.value)}
                placeholder="Text trích xuất từ ảnh sẽ hiển thị ở đây..."
                style={{
                  width: "100%",
                  minHeight: "400px",
                  backgroundColor: "#1f1f1f",
                  color: "#fff",
                  border: "1px solid #434343",
                  whiteSpace: "pre-line", // Đảm bảo giữ nguyên xuống dòng
                  fontSize: "16px",
                  lineHeight: "1.6",
                }}
              />
            </div>
          </Col>
        </Row>
      </div>
    </div>
  );
}

export default App;
