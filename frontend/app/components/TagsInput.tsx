/**
 * Tags input component with tag chips.
 */

'use client';

import { useState, KeyboardEvent } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface TagsInputProps {
  value: string;
  onChange: (tags: string) => void;
  placeholder?: string;
}

export default function TagsInput({ value, onChange, placeholder = 'Add tags...' }: TagsInputProps) {
  const [inputValue, setInputValue] = useState('');

  const tags = value ? value.split(',').map(t => t.trim()).filter(Boolean) : [];

  const addTag = (tag: string) => {
    const trimmedTag = tag.trim();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      const newTags = [...tags, trimmedTag];
      onChange(newTags.join(','));
      setInputValue('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    const newTags = tags.filter(t => t !== tagToRemove);
    onChange(newTags.join(','));
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addTag(inputValue);
    } else if (e.key === 'Backspace' && !inputValue && tags.length > 0) {
      removeTag(tags[tags.length - 1]);
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap gap-2 p-2 bg-slate-50 dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg min-h-[42px]">
        <AnimatePresence>
          {tags.map((tag) => (
            <motion.span
              key={tag}
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              className="inline-flex items-center px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 rounded-md text-sm"
            >
              <span className="mr-1">#</span>
              {tag}
              <button
                type="button"
                onClick={() => removeTag(tag)}
                className="ml-1 hover:text-blue-600 dark:hover:text-blue-300"
              >
                ×
              </button>
            </motion.span>
          ))}
        </AnimatePresence>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => inputValue && addTag(inputValue)}
          placeholder={tags.length === 0 ? placeholder : ''}
          className="flex-1 min-w-[120px] bg-transparent border-none outline-none text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500"
        />
      </div>
      <p className="text-xs text-slate-500 dark:text-slate-400">
        Press Enter or comma to add tags. Click × to remove.
      </p>
    </div>
  );
}

export function TagsList({ tags }: { tags: string | null }) {
  if (!tags) return null;

  const tagArray = tags.split(',').map(t => t.trim()).filter(Boolean);

  if (tagArray.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-1">
      {tagArray.map((tag) => (
        <span
          key={tag}
          className="inline-flex items-center px-2 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 rounded text-xs"
        >
          <span className="mr-0.5">#</span>
          {tag}
        </span>
      ))}
    </div>
  );
}
