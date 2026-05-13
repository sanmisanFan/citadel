import { useState, useEffect } from "react";
import { Input, Button } from 'antd';
import { PlusOutlined, MinusOutlined } from '@ant-design/icons';

// Dynamically create text inputs for fields with multiple values (e.g., authors)
const TextInputArray = ({ updateCallback, unitName, initialValues }) => {
    const [content, setContent] = useState([""]);

    // Re-seed contents when caller provides a fresh set (e.g. auto-extracted authors).
    useEffect(() => {
        if (initialValues && initialValues.length > 0) {
            setContent([...initialValues]);
        }
    }, [initialValues]);

    const updateContent = (e, i) => {
        content[i] = e.currentTarget.value;
        setContent([...content]);
    };

    const onAddButton = () => {
        setContent(previous => [...previous, ""]);
    };

    const onRemoveButton = (index) => {
        if (content.length > 1) {
            setContent(previous => previous.filter((_, i) => i !== index));
        }
    };

    useEffect(() => {
        if (updateCallback) {
            updateCallback([...content]);
        }
    }, [content, updateCallback]);

    return (
        <div className="author-input-container">
            <div className="author-inputs">
                {content.map((s, i) => (
                    <div key={i} className="author-row">
                        <Input
                            size="large"
                            placeholder={`${unitName} ${i + 1}`}
                            value={s}
                            onChange={(e) => updateContent(e, i)}
                        />
                        {content.length > 1 && (
                            <Button
                                type="text"
                                icon={<MinusOutlined />}
                                onClick={() => onRemoveButton(i)}
                                style={{ color: '#8c9bab' }}
                            />
                        )}
                    </div>
                ))}
            </div>
            <div className="author-actions">
                <Button
                    type="dashed"
                    icon={<PlusOutlined />}
                    onClick={onAddButton}
                >
                    Add {unitName}
                </Button>
            </div>
        </div>
    );
};

export default TextInputArray;
