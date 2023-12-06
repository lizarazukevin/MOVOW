import React from 'react'
import styled from 'styled-components'
import { Link } from 'react-router-dom'

const ButtonComponent = styled.button`
    background-color: 
    background-color: #F3E5AB;
    border: none;
    padding: 10px;
    margin: 10px;
    border-radius: 8px;
    cursor: pointer;
`;

const StyledLink = styled(Link)`
    text-decoration: none;
`;

const Button = ({to, type, variant, className, id, onClick, children}) => {
    return (
        <StyledLink to={to}>
            <ButtonComponent
                type={type ? type: "button"}
                variant={variant}
                className={className ? `btn-component ${className}` : "btn-component"}
                id={id}
                onClick={onClick}
            >
                {children}
            </ButtonComponent>
        </StyledLink>
    );
};

export default Button