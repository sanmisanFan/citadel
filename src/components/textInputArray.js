import { useState, useEffect } from "react";

import { Input, Button, Flex } from 'antd';

// dynamically create text inputs for text fields that have multiple inputs e.g. authors
const TextInputArray = ({ updateCallback, unitName }) => {
    const [content, setContent] = useState([""]);

    const updateContent = (e, i) => {
        content[i] = e.currentTarget.value;
        setContent([...content]);
    };

    const onAddButton = (e) => {
        setContent(previous => [...previous, ""]);
    };

    const onRemoveButton = (e) => {
        if (content.length > 1) {
            setContent(previous => previous.slice(0, -1));
        }
    };

    useEffect(() => {
        if (updateCallback) {
            updateCallback([...content]);
        }
    }, [content, updateCallback]);

    return <Flex vertical gap="small">
        <Flex>
            <Button type="primary" onClick={onAddButton}>+</Button>
            <Button type="primary" disabled={content.length === 1} onClick={onRemoveButton}>-</Button>
        </Flex>
        {content.map((s, i) => <Input key={i} placeholder={`${unitName} ${i}`} value={s} onChange={(e) => updateContent(e, i)} />)}
    </Flex>
};

export default TextInputArray;
